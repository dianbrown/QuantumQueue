"""Interactive main window for Page Replacement Algorithms practice."""

from typing import List, Optional
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QComboBox, QLabel,
    QHeaderView, QMessageBox, QSpinBox, QLineEdit, QScrollArea, QMenu,
    QFrame, QApplication
)
from PySide6.QtCore import Qt, QMimeData, QPoint
from PySide6.QtGui import QFont, QColor, QDrag, QPainter, QPixmap
import random

# Import PRA algorithms and models
from PRA.algorithms.fifo import FIFOReplacer
from PRA.algorithms.lru import LRUReplacer
from PRA.algorithms.optimal import OptimalReplacer
from PRA.algorithms.second_chance import SecondChanceReplacer
from PRA.algorithms.clock import ClockReplacer
from PRA.algorithms.base_replacer import PageReplacementResult
from PRA.models.frame import Frame


class DraggableFrameBlock(QLabel):
    """Draggable frame block for queue visualization."""
    
    def __init__(self, frame_id: str, parent=None):
        super().__init__(parent)
        self.frame_id = frame_id
        self.rbit = False  # R-bit state (False = 0, True = 1)
        self.theme_colors = {}  # Store theme colors
        self.update_display()
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(60, 30)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.update_style()
        
    def update_display(self):
        """Update the text display with R-bit indicator."""
        rbit_indicator = "●" if self.rbit else "○"
        self.setText(f"F{self.frame_id} {rbit_indicator}")
        
    def set_theme_colors(self, theme_colors: dict):
        """Set theme colors for the block."""
        self.theme_colors = theme_colors
        self.update_style()
        
    def update_style(self):
        """Update the stylesheet."""
        # Use theme colors if available, otherwise use defaults
        bg_color = self.theme_colors.get('queue_block_bg', '#4a90e2')
        border_color = self.theme_colors.get('queue_block_border', '#357abd')
        text_color = self.theme_colors.get('queue_block_text', 'white')
        
        # Calculate hover color (slightly lighter)
        hover_color = self._lighten_color(bg_color, 0.1)
        
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border: 2px solid {border_color};
                border-radius: 3px;
                font-weight: bold;
                font-size: 12px;
            }}
            QLabel:hover {{
                background-color: {hover_color};
            }}
        """)
    
    def _lighten_color(self, hex_color: str, factor: float) -> str:
        """Lighten a hex color by a factor (0.0 to 1.0)."""
        # Remove '#' if present
        hex_color = hex_color.lstrip('#')
        
        # Convert to RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Lighten
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"
        
    def mousePressEvent(self, event):
        """Handle mouse press for drag initiation."""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
            
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging."""
        if not (event.buttons() & Qt.LeftButton):
            return
            
        if ((event.pos() - self.drag_start_position).manhattanLength() < 
            QApplication.startDragDistance()):
            return
            
        # Start drag operation
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.frame_id)
        drag.setMimeData(mime_data)
        
        # Create drag pixmap - fill with transparent first to initialize paint device
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.transparent)
        self.render(pixmap)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        
        # Execute drag
        drag.exec(Qt.MoveAction)
        
    def show_context_menu(self, position):
        """Show context menu for R-bit control."""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #555;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 20px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #4a90e2;
            }
        """)
        
        if self.rbit:
            action = menu.addAction("Set R-bit to 0 (○)")
        else:
            action = menu.addAction("Set R-bit to 1 (●)")
        
        action.triggered.connect(self.toggle_rbit)
        menu.exec(self.mapToGlobal(position))
        
    def toggle_rbit(self):
        """Toggle the R-bit state."""
        self.rbit = not self.rbit
        self.update_display()
        
    def get_rbit_state(self) -> bool:
        """Get the current R-bit state (True = 1, False = 0)."""
        return self.rbit
        
    def set_rbit_state(self, state: bool):
        """Set the R-bit state (True = 1, False = 0)."""
        self.rbit = state
        self.update_display()


class QueueVisualizationWidget(QWidget):
    """Widget for visualizing and managing the FIFO queue order."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.frame_blocks = []
        self.theme_colors = {}  # Store theme colors
        self.init_ui()
        
    def init_ui(self):
        """Initialize the queue visualization UI."""
        layout = QVBoxLayout(self)
        
        # Title
        self.title = QLabel("Queue Order:")
        self.title.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(self.title)
        
        # Queue container
        self.queue_container = QWidget()
        self.queue_layout = QHBoxLayout(self.queue_container)
        self.queue_layout.setSpacing(5)
        self.queue_layout.setContentsMargins(10, 10, 10, 10)
        
        # Style the container
        self.queue_container.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 2px dashed #ccc;
                border-radius: 5px;
                min-height: 60px;
            }
        """)
        self.queue_container.setAcceptDrops(True)
        self.queue_container.dragEnterEvent = self.drag_enter_event
        self.queue_container.dragMoveEvent = self.drag_move_event
        self.queue_container.dropEvent = self.drop_event
        
        layout.addWidget(self.queue_container)
    
    def set_theme_colors(self, theme_colors: dict):
        """Set theme colors for the queue visualization."""
        self.theme_colors = theme_colors
        
        # Update container style
        container_bg = theme_colors.get('queue_container_bg', '#f0f0f0')
        container_border = theme_colors.get('queue_container_border', '#ccc')
        
        self.queue_container.setStyleSheet(f"""
            QWidget {{
                background-color: {container_bg};
                border: 2px dashed {container_border};
                border-radius: 5px;
                min-height: 60px;
            }}
        """)
        
        # Update all frame blocks
        for block in self.frame_blocks:
            block.set_theme_colors(theme_colors)
        
    def update_frames(self, frames: List[Frame]):
        """Update the queue with current frames."""
        # Clear existing blocks
        for block in self.frame_blocks:
            block.setParent(None)
        self.frame_blocks.clear()
        
        # Sort frames by load time to show initial FIFO order
        sorted_frames = sorted(frames, key=lambda f: f.load_time)
        
        # Create new blocks
        for frame in sorted_frames:
            block = DraggableFrameBlock(frame.frame_id, self.queue_container)
            # Apply theme colors if available
            if self.theme_colors:
                block.set_theme_colors(self.theme_colors)
            self.frame_blocks.append(block)
            self.queue_layout.addWidget(block, alignment=Qt.AlignVCenter)
            
    def drag_enter_event(self, event):
        """Handle drag enter event."""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            
    def drag_move_event(self, event):
        """Handle drag move event."""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            
    def drop_event(self, event):
        """Handle drop event to reorder queue."""
        if event.mimeData().hasText():
            frame_id = event.mimeData().text()
            drop_position = event.pos()
            
            # Find the frame block being dragged
            dragged_block = None
            dragged_index = -1
            for i, block in enumerate(self.frame_blocks):
                if block.frame_id == frame_id:
                    dragged_block = block
                    dragged_index = i
                    break
                    
            if dragged_block and dragged_index >= 0:
                # Calculate insertion position before removing the item
                insert_index = self.calculate_insert_position(drop_position, dragged_index)
                
                # Only proceed if the position actually changes
                if insert_index != dragged_index:
                    # Remove the block
                    self.queue_layout.removeWidget(dragged_block)
                    self.frame_blocks.remove(dragged_block)
                    
                    # Adjust insert index if necessary (since we removed an item)
                    if insert_index > dragged_index:
                        insert_index -= 1
                    
                    # Ensure insert_index is within bounds
                    insert_index = max(0, min(insert_index, len(self.frame_blocks)))
                    
                    # Insert at new position with vertical center alignment
                    self.queue_layout.insertWidget(insert_index, dragged_block, alignment=Qt.AlignVCenter)
                    self.frame_blocks.insert(insert_index, dragged_block)
                
            event.acceptProposedAction()
            
    def calculate_insert_position(self, drop_pos: QPoint, dragged_index: int = -1) -> int:
        """Calculate where to insert the dropped frame."""
        for i, block in enumerate(self.frame_blocks):
            # Skip the dragged block itself when calculating position
            if i == dragged_index:
                continue
            if drop_pos.x() < block.x() + block.width() // 2:
                return i
        return len(self.frame_blocks)
        
    def get_queue_order(self) -> List[str]:
        """Get current queue order as list of frame IDs."""
        return [block.frame_id for block in self.frame_blocks]
    
    def get_rbit_states(self) -> dict:
        """Get R-bit states for all frames in the queue."""
        return {block.frame_id: block.get_rbit_state() for block in self.frame_blocks}
    
    def set_rbit_state(self, frame_id: str, state: bool):
        """Set R-bit state for a specific frame."""
        for block in self.frame_blocks:
            if block.frame_id == frame_id:
                block.set_rbit_state(state)
                break
    
    def reset_all_rbits(self):
        """Reset all R-bits to 0."""
        for block in self.frame_blocks:
            block.set_rbit_state(False)


class PRAMainWindow(QWidget):
    """Interactive main window for Page Replacement Algorithms practice."""
    
    def __init__(self):
        super().__init__()
        self.frames: List[Frame] = []
        self.page_sequence: List[str] = []
        self.solution_table: Optional[QTableWidget] = None
        self.solution_result: Optional[PageReplacementResult] = None
        self.current_solution: List[List[str]] = []
        self.is_locked = False
        self.results_label: Optional[QLabel] = None
        self.results_scroll_area: Optional[QScrollArea] = None
        self.algorithm_name_label: Optional[QLabel] = None
        self.queue_widget: Optional[QueueVisualizationWidget] = None
        
        # Initialize algorithms
        self.algorithms = {
            "FIFO": FIFOReplacer(),
            "LRU": LRUReplacer(),
            "Optimal": OptimalReplacer(),
            "Second Chance": SecondChanceReplacer(),
            "Clock": ClockReplacer()
        }
        
        self.init_ui()
        self.add_sample_frames()
        
    def init_ui(self):
        """Initialize the user interface."""
        main_layout = QVBoxLayout(self)
        
        # Top controls
        controls_layout = QHBoxLayout()
        
        # Algorithm selection
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(list(self.algorithms.keys()))
        self.algorithm_combo.setMinimumWidth(250)
        self.algorithm_combo.setStyleSheet("""
            QComboBox {
                font-size: 13px;
                padding: 6px;
            }
        """)
        self.algorithm_combo.currentTextChanged.connect(self.on_algorithm_changed)
        controls_layout.addWidget(QLabel("Algorithm:"))
        controls_layout.addWidget(self.algorithm_combo)
        
        # Page sequence input
        self.page_input = QLineEdit()
        self.page_input.setPlaceholderText("Enter page sequence (e.g., 7,0,1,2,0,3,0,4)")
        self.page_input.textChanged.connect(self.on_page_sequence_changed)
        controls_layout.addWidget(QLabel("Pages:"))
        controls_layout.addWidget(self.page_input)
        
        controls_layout.addStretch()
        main_layout.addLayout(controls_layout)
        
        # Fixed spacing below controls (like CPU page)
        main_layout.addSpacing(20)
        
        # Solution table (unified - combines frame data + solution grid)
        self.setup_solution_table()
        main_layout.addWidget(self.solution_table, stretch=1)
        
        # Spacing between table and queue
        main_layout.addSpacing(10)
        
        # Queue visualization widget - centered
        queue_container = QHBoxLayout()
        queue_container.addStretch()
        self.queue_widget = QueueVisualizationWidget()
        self.queue_widget.setMaximumWidth(600)  # Limit width for centering
        queue_container.addWidget(self.queue_widget)
        queue_container.addStretch()
        main_layout.addLayout(queue_container)
        
        # Spacing between queue and console
        main_layout.addSpacing(10)
        
        # Results display with scroll area
        self.results_label = QLabel("")
        self.results_label.setWordWrap(True)
        self.results_label.setStyleSheet("""
            QLabel {
                background-color: #2b2b2b;
                border: none;
                padding: 10px;
                font-family: monospace;
                color: white;
            }
        """)
        
        # Create scroll area for results
        self.results_scroll_area = QScrollArea()
        self.results_scroll_area.setWidget(self.results_label)
        self.results_scroll_area.setWidgetResizable(True)
        self.results_scroll_area.setMinimumHeight(100)
        self.results_scroll_area.setMaximumHeight(150)
        self.results_scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #555;
                border-radius: 5px;
                background-color: #2b2b2b;
            }
        """)
        
        main_layout.addWidget(self.results_scroll_area)
        
        # Spacing between console and buttons
        main_layout.addSpacing(15)
        
        # Buttons section - centered at bottom
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        # Button rows container
        buttons_container = QVBoxLayout()
        buttons_container.setSpacing(10)
        
        # Uniform button size - all buttons exactly the same (matching CPU page)
        btn_width = 130
        btn_height = 40
        btn_style = f"min-width: {btn_width}px; max-width: {btn_width}px; min-height: {btn_height}px; max-height: {btn_height}px;"
        
        # First row of buttons
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(10)
        
        add_frame_btn = QPushButton("Add Frame")
        add_frame_btn.clicked.connect(self.add_frame)
        add_frame_btn.setFixedWidth(btn_width)
        add_frame_btn.setFixedHeight(btn_height)
        add_frame_btn.setStyleSheet(btn_style)
        
        delete_frame_btn = QPushButton("Delete Frame")
        delete_frame_btn.clicked.connect(self.delete_frame)
        delete_frame_btn.setFixedWidth(btn_width)
        delete_frame_btn.setFixedHeight(btn_height)
        delete_frame_btn.setStyleSheet(btn_style)
        
        randomize_btn = QPushButton("Randomize")
        randomize_btn.clicked.connect(self.generate_random_problem)
        randomize_btn.setFixedWidth(btn_width)
        randomize_btn.setFixedHeight(btn_height)
        randomize_btn.setStyleSheet(btn_style)
        
        row1_layout.addWidget(add_frame_btn)
        row1_layout.addWidget(delete_frame_btn)
        row1_layout.addWidget(randomize_btn)
        buttons_container.addLayout(row1_layout)
        
        # Second row of buttons
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(10)
        
        check_btn = QPushButton("Check Solution")
        check_btn.clicked.connect(self.check_solution)
        check_btn.setFixedWidth(btn_width)
        check_btn.setFixedHeight(btn_height)
        check_btn.setStyleSheet(btn_style)
        
        show_btn = QPushButton("Show Solution")
        show_btn.clicked.connect(self.show_solution)
        show_btn.setFixedWidth(btn_width)
        show_btn.setFixedHeight(btn_height)
        show_btn.setStyleSheet(btn_style)
        
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_solution)
        reset_btn.setFixedWidth(btn_width)
        reset_btn.setFixedHeight(btn_height)
        reset_btn.setStyleSheet(btn_style)
        
        row2_layout.addWidget(check_btn)
        row2_layout.addWidget(show_btn)
        row2_layout.addWidget(reset_btn)
        buttons_container.addLayout(row2_layout)
        
        buttons_layout.addLayout(buttons_container)
        buttons_layout.addStretch()
        
        main_layout.addLayout(buttons_layout)
        
        # Bottom spacing
        main_layout.addSpacing(15)
        
    def setup_solution_table(self):
        """Set up the unified solution grid for frame data and page replacement visualization."""
        self.solution_table = QTableWidget(0, 0)
        self.solution_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.solution_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.solution_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.solution_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Connect cell events
        self.solution_table.cellClicked.connect(self.on_cell_clicked)
        self.solution_table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.solution_table.itemChanged.connect(self.on_solution_table_changed)
        
        # Enable context menu
        self.solution_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.solution_table.customContextMenuRequested.connect(self.show_context_menu)
        
        # Set row height and column width
        self.solution_table.verticalHeader().setDefaultSectionSize(30)
        
    def add_sample_frames(self):
        """Add sample frames for demonstration."""
        sample_frames = [
            Frame("3", 7, "2"),
            Frame("2", 6, "4"),
            Frame("1", 21, "8"),
            Frame("0", 12, "5"),
        ]
        self.frames = sample_frames
        self.update_frame_table()
        
        # Set sample page sequence (using 1-15 range)
        sample_template = "9,7,8,3,5,7,7,9,6,3,3,7,9,7,4,6,7,8,3,2,5,4,7,6,4,2,3,4,3,2,7,7"
        self.page_input.setText(f"{sample_template}")
        self.parse_page_sequence(f"{sample_template}")
        
    def update_frame_table(self):
        """Update the frame display with current frames (now uses solution_table)."""
        # Refresh the solution table which includes frame data
        self.update_solution_table()
        
        # Update queue visualization
        if self.queue_widget:
            self.queue_widget.update_frames(self.frames)
    
    def on_frame_table_changed(self, item):
        """Handle when frame table data is edited by user."""
        # Read the updated frame data and refresh solution table
        self.read_frame_table()
        self.update_solution_table()
        
    def on_solution_table_changed(self, item):
        """Handle when solution table data is edited (frame columns 1-2)."""
        if item is None:
            return
        col = item.column()
        row = item.row()
        
        # Only react to changes in editable frame columns (1: Load Time, 2: Page in Memory)
        if col not in (1, 2):
            return
        # Skip algorithm and legend rows
        if row >= len(self.frames):
            return
            
        # Update frame data from table
        if len(self.frames) > row:
            if col == 1:  # Load Time
                try:
                    self.frames[row].load_time = int(item.text()) if item.text() else 0
                except ValueError:
                    pass
            elif col == 2:  # Page in Memory
                self.frames[row].pages_in_memory = item.text()
            
            # Update queue visualization
            if self.queue_widget:
                self.queue_widget.update_frames(self.frames)
        
    def generate_random_problem(self):
        """Generate random frame data and page sequence for practice."""
        # Generate random number of frames (3-6 frames)
        num_frames = random.randint(3, 6)
        
        # Clear existing frames
        self.frames.clear()
        
        # Generate unique load times for all frames (1-20, no duplicates)
        available_load_times = list(range(1, 21))  # 1 to 20
        random.shuffle(available_load_times)
        selected_load_times = available_load_times[:num_frames]
        
        # Generate random frames with descending IDs
        used_pages = set()
        for i in range(num_frames):
            frame_id = str(num_frames - 1 - i)  # Descending order: 5,4,3,2,1,0
            load_time = selected_load_times[i]  # Unique load time
            
            # Generate unique page for initial state (1-15)
            page = random.randint(1, 15)
            while page in used_pages:
                page = random.randint(1, 15)
            used_pages.add(page)
            
            frame = Frame(frame_id, load_time, str(page))
            self.frames.append(frame)
        
        # Generate random page sequence (10-30 pages, values 1-15)
        sequence_length = random.randint(10, 30)
        page_sequence = []
        
        for _ in range(sequence_length):
            page = random.randint(1, 15)
            page_sequence.append(str(page))
        
        # Update UI
        self.update_frame_table()
        
        # Set the page sequence
        page_sequence_str = ",".join(page_sequence)
        self.page_input.setText(page_sequence_str)
        self.parse_page_sequence(page_sequence_str)
        
        # Clear any existing solution
        self.solution_result = None
        self.clear_results()
        
    def clear_results(self):
        """Clear the results display."""
        if self.results_label:
            self.results_label.setText("No results yet. Generate a solution to see statistics.")
            
    def read_frame_table(self):
        """Read frame data from the solution table (unified table)."""
        self.frames = []
        # Read from solution_table columns 0, 1, 2 (Frame ID, Load Time, Page in Memory)
        num_frame_rows = self.solution_table.rowCount() - 2  # Exclude algorithm and legend rows
        for i in range(num_frame_rows):
            frame_id_item = self.solution_table.item(i, 0)
            load_time_item = self.solution_table.item(i, 1)
            pages_item = self.solution_table.item(i, 2)
            
            if frame_id_item and load_time_item and pages_item:
                try:
                    frame_id = frame_id_item.text()
                    load_time = int(load_time_item.text()) if load_time_item.text() else 0
                    pages = pages_item.text()
                    
                    self.frames.append(Frame(frame_id, load_time, pages))
                except ValueError:
                    # Skip invalid entries
                    pass
                    
    def parse_page_sequence(self, sequence_text: str):
        """Parse page sequence from text input."""
        try:
            if not sequence_text.strip():
                self.page_sequence = []
                return
                
            # Split by comma and clean up
            pages = [page.strip() for page in sequence_text.split(',') if page.strip()]
            self.page_sequence = pages
            self.update_solution_table()
            
        except Exception as e:
            QMessageBox.warning(self, "Invalid Input", f"Error parsing page sequence: {e}")
            self.page_sequence = []
            
    def on_page_sequence_changed(self):
        """Handle page sequence input change."""
        self.parse_page_sequence(self.page_input.text())
        
    def on_algorithm_changed(self):
        """Handle algorithm selection change."""
        algorithm = self.algorithm_combo.currentText()
        
        # Update the algorithm name in the solution table if it exists
        if self.solution_table and self.solution_table.rowCount() > len(self.frames):
            algorithm_row = len(self.frames)
            alg_name_item = QTableWidgetItem(algorithm)
            alg_name_item.setFlags(alg_name_item.flags() & ~Qt.ItemIsEditable)
            alg_name_item.setTextAlignment(Qt.AlignCenter)
            self.solution_table.setItem(algorithm_row, 2, alg_name_item)  # Column 2 = Page in Memory
        
        self.reset_solution()
        
    def update_solution_table(self):
        """Update the solution table with current data."""
        if not self.page_sequence or not self.frames:
            self.solution_table.setRowCount(0)
            self.solution_table.setColumnCount(0)
            return
            
        # Setup table dimensions
        num_frames = len(self.frames)
        num_pages = len(self.page_sequence)
        num_rows = num_frames + 2  # frames + algorithm + legend rows
        num_cols = num_pages + 3   # pages + Frame ID + Load Time + Page in Memory columns
        
        self.solution_table.setRowCount(num_rows)
        self.solution_table.setColumnCount(num_cols)
        
        # Set up headers - include Load Time
        headers = ["Frame ID", "Load Time", "Page in Memory"] + self.page_sequence
        self.solution_table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        self.solution_table.setColumnWidth(0, 70)   # Frame ID column
        self.solution_table.setColumnWidth(1, 75)   # Load Time column
        self.solution_table.setColumnWidth(2, 115)  # Page in Memory column
        for i in range(3, num_cols):
            self.solution_table.setColumnWidth(i, 35)  # Page columns
        
        # Hide the vertical header (row numbers)
        self.solution_table.verticalHeader().setVisible(False)
            
        # Fill initial data
        self.fill_solution_table_structure()
        
    def fill_solution_table_structure(self):
        """Fill the basic structure of the solution table."""
        if not self.frames:
            return
        
        # Block signals to prevent itemChanged from corrupting frame data
        self.solution_table.blockSignals(True)
            
        # Clear existing data
        for row in range(self.solution_table.rowCount()):
            for col in range(self.solution_table.columnCount()):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignCenter)
                self.solution_table.setItem(row, col, item)
                
        # Frame rows
        for frame_idx, frame in enumerate(self.frames):
            # Frame ID column (read-only)
            frame_item = QTableWidgetItem(frame.frame_id)
            frame_item.setFlags(frame_item.flags() & ~Qt.ItemIsEditable)
            frame_item.setTextAlignment(Qt.AlignCenter)
            self.solution_table.setItem(frame_idx, 0, frame_item)
            
            # Load Time column (editable)
            load_item = QTableWidgetItem(str(frame.load_time))
            load_item.setTextAlignment(Qt.AlignCenter)
            self.solution_table.setItem(frame_idx, 1, load_item)
            
            # Page in Memory column (editable)
            page_item = QTableWidgetItem(frame.pages_in_memory)
            page_item.setTextAlignment(Qt.AlignCenter)
            self.solution_table.setItem(frame_idx, 2, page_item)
            
            # Page columns - these are interactive (start at column 3)
            for page_idx in range(len(self.page_sequence)):
                col_idx = page_idx + 3  # Offset by 3 for Frame ID, Load Time, Page in Memory
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QColor("white"))
                if not self.is_locked:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.solution_table.setItem(frame_idx, col_idx, item)
                
        # Algorithm row
        algorithm_row = len(self.frames)
        alg_label_item = QTableWidgetItem("Algorithm:")
        alg_label_item.setFlags(alg_label_item.flags() & ~Qt.ItemIsEditable)
        alg_label_item.setTextAlignment(Qt.AlignCenter)
        self.solution_table.setItem(algorithm_row, 0, alg_label_item)
        
        alg_name_item = QTableWidgetItem(self.algorithm_combo.currentText())
        alg_name_item.setFlags(alg_name_item.flags() & ~Qt.ItemIsEditable)
        alg_name_item.setTextAlignment(Qt.AlignCenter)
        self.solution_table.setItem(algorithm_row, 2, alg_name_item)  # Column 2 = Page in Memory
        
        # Legend row
        legend_row = len(self.frames) + 1
        legend_label_item = QTableWidgetItem("Legend:")
        legend_label_item.setFlags(legend_label_item.flags() & ~Qt.ItemIsEditable)
        legend_label_item.setTextAlignment(Qt.AlignCenter)
        self.solution_table.setItem(legend_row, 0, legend_label_item)
        
        # Add legend items (start at column 3 - first page column)
        if self.solution_table.columnCount() > 3:
            hit_item = QTableWidgetItem("Hit")
            hit_item.setFlags(hit_item.flags() & ~Qt.ItemIsEditable)
            hit_item.setTextAlignment(Qt.AlignCenter)
            hit_item.setBackground(QColor("#4caf50"))
            hit_item.setForeground(QColor("white"))
            self.solution_table.setItem(legend_row, 3, hit_item)
            
        if self.solution_table.columnCount() > 4:
            fault_item = QTableWidgetItem("Fault")
            fault_item.setFlags(fault_item.flags() & ~Qt.ItemIsEditable)
            fault_item.setTextAlignment(Qt.AlignCenter)
            fault_item.setBackground(QColor("#f44336"))
            fault_item.setForeground(QColor("white"))
            self.solution_table.setItem(legend_row, 4, fault_item)
        
        # Unblock signals after table is populated
        self.solution_table.blockSignals(False)
            
    def on_cell_clicked(self, row: int, col: int):
        """Handle cell click events."""
        if col < 3 or self.is_locked:  # Skip Frame ID, Load Time, and Page in Memory columns
            return
            
        if row >= len(self.frames):  # Skip algorithm and legend rows
            return
            
        item = self.solution_table.item(row, col)
        if item is None:
            return
            
        # Get the page that should be in this cell
        page_idx = col - 3  # Offset by 3 for Frame ID, Load Time, Page in Memory
        if page_idx < len(self.page_sequence):
            page_id = self.page_sequence[page_idx]
            
            # Toggle cell content and color
            current_text = item.text()
            if current_text == page_id:
                # Clear the cell
                item.setText("")
                item.setBackground(QColor("white"))
                item.setForeground(QColor("black"))
            else:
                # Set the page ID in the cell
                item.setText(page_id)
                # User will need to set color manually or through context menu
                item.setBackground(QColor("white"))
                item.setForeground(QColor("black"))
                
    def on_cell_double_clicked(self, row: int, col: int):
        """Handle cell double-click to toggle colors."""
        if col < 3 or self.is_locked or row >= len(self.frames):  # Skip first 3 columns
            return
            
        item = self.solution_table.item(row, col)
        if item is None or not item.text():
            return
            
        # Cycle through colors: white -> green (hit) -> red (fault) -> white
        current_color = item.background().color().name().lower()
        
        if current_color == "#ffffff" or current_color == "white":
            # Set to green (hit)
            item.setBackground(QColor("#4caf50"))
            item.setForeground(QColor("white"))
        elif current_color == "#4caf50":
            # Set to red (fault)
            item.setBackground(QColor("#f44336"))
            item.setForeground(QColor("white"))
        else:
            # Set back to white
            item.setBackground(QColor("white"))
            item.setForeground(QColor("black"))
            
    def show_context_menu(self, position):
        """Show context menu for cell operations."""
        item = self.solution_table.itemAt(position)
        if item is None or self.is_locked:
            return
            
        row = item.row()
        col = item.column()
        
        if col < 3 or row >= len(self.frames):  # Skip first 3 columns
            return
            
        menu = QMenu(self)
        
        # Add page action
        page_idx = col - 3  # Offset by 3 for Frame ID, Load Time, Page in Memory
        if page_idx < len(self.page_sequence):
            page_id = self.page_sequence[page_idx]
            add_page_action = menu.addAction(f"Add Page {page_id}")
            add_page_action.triggered.connect(lambda: self.add_page_to_cell(row, col, page_id))
            
        # Color actions
        menu.addSeparator()
        hit_action = menu.addAction("Mark as Hit (Green)")
        hit_action.triggered.connect(lambda: self.set_cell_color(row, col, "hit"))
        
        fault_action = menu.addAction("Mark as Fault (Red)")
        fault_action.triggered.connect(lambda: self.set_cell_color(row, col, "fault"))
        
        clear_action = menu.addAction("Clear Cell")
        clear_action.triggered.connect(lambda: self.clear_cell(row, col))
        
        menu.exec(self.solution_table.mapToGlobal(position))
        
    def add_page_to_cell(self, row: int, col: int, page_id: str):
        """Add page to a specific cell."""
        item = self.solution_table.item(row, col)
        if item:
            item.setText(page_id)
            
    def set_cell_color(self, row: int, col: int, color_type: str):
        """Set cell color for hit/fault indication."""
        item = self.solution_table.item(row, col)
        if item:
            if color_type == "hit":
                item.setBackground(QColor("#4caf50"))
                item.setForeground(QColor("white"))
            elif color_type == "fault":
                item.setBackground(QColor("#f44336"))
                item.setForeground(QColor("white"))
                
    def clear_cell(self, row: int, col: int):
        """Clear a cell."""
        item = self.solution_table.item(row, col)
        if item:
            item.setText("")
            item.setBackground(QColor("white"))
            item.setForeground(QColor("black"))
            
    def add_frame(self):
        """Add a new frame to the top of the list."""
        # Read current frame table data first
        self.read_frame_table()
        
        # Find the highest frame ID and add 1
        existing_ids = [int(frame.frame_id) for frame in self.frames if frame.frame_id.isdigit()]
        if existing_ids:
            max_id = max(existing_ids)
            frame_id = str(max_id + 1)
        else:
            # No existing frames, start with 0
            frame_id = "0"
        
        new_frame = Frame(frame_id, 0, "")
        # Insert at the beginning to show at top
        self.frames.insert(0, new_frame)
        self.update_frame_table()
        self.update_solution_table()
        
    def delete_frame(self):
        """Delete the top frame."""
        if self.frames:
            # Read current frame table data first
            self.read_frame_table()
            # Remove the first frame (top of the list)
            self.frames.pop(0)
            self.update_frame_table()
            self.update_solution_table()
            
    def check_solution(self):
        """Check the student's solution against the correct solution."""
        self.read_frame_table()
        
        if not self.page_sequence or not self.frames:
            QMessageBox.warning(self, "No Data", "Please enter page sequence and frame data.")
            return
            
        # Get the selected algorithm
        algorithm_name = self.algorithm_combo.currentText()
        algorithm = self.algorithms[algorithm_name]
        
        # Calculate correct solution using frame data
        if hasattr(algorithm, 'replace_pages_with_frames'):
            self.solution_result = algorithm.replace_pages_with_frames(self.page_sequence, self.frames)
        else:
            self.solution_result = algorithm.replace_pages(self.page_sequence, len(self.frames))
        
        # Get student's solution from the table
        student_solution = self.get_student_solution()
        
        # Compare solutions
        self.compare_solutions(student_solution)
        
    def get_student_solution(self):
        """Get the student's solution from the table."""
        solution = []
        
        if not self.frames:
            return solution
            
        # Get each page access
        for page_idx in range(len(self.page_sequence)):
            col_idx = page_idx + 3  # Offset by 3 for Frame ID, Load Time, Page in Memory
            page_state = {}
            
            for frame_idx in range(len(self.frames)):
                item = self.solution_table.item(frame_idx, col_idx)
                if item and item.text():
                    page_state[frame_idx] = {
                        'page': item.text(),
                        'is_hit': item.background().color().name().lower() == "#4caf50"
                    }
                    
            solution.append(page_state)
            
        return solution
        
    def compare_solutions(self, student_solution):
        """Compare student hit/fault identification with correct solution."""
        if not self.solution_result:
            return
            
        correct_count = 0
        total_checks = len(self.page_sequence)
        errors = []
        
        # Check each page request (column)
        for page_idx, page_id in enumerate(self.page_sequence):
            if page_idx < len(self.solution_result.accesses):
                access = self.solution_result.accesses[page_idx]
                expected_is_hit = access.is_hit
                
                # Find which frame should contain the page and determine expected frame location
                expected_frame_idx = None
                if expected_is_hit:
                    # For hits, find which frame already has this page
                    for frame_idx, page_in_frame in enumerate(access.frames_state):
                        if page_in_frame == page_id:
                            expected_frame_idx = frame_idx
                            break
                else:
                    # For faults, find which frame gets the new page after replacement
                    for frame_idx, page_in_frame in enumerate(access.frames_state):
                        if page_in_frame == page_id:
                            expected_frame_idx = frame_idx
                            break
                
                # Check student's markings in this column
                col_idx = page_idx + 3  # Offset by 3 for Frame ID, Load Time, Page in Memory
                student_markings = []
                
                for frame_idx in range(len(self.frames)):
                    item = self.solution_table.item(frame_idx, col_idx)
                    if item and item.text() == page_id:
                        color = item.background().color().name().lower()
                        is_hit_marked = (color == "#4caf50")  # green
                        is_fault_marked = (color == "#f44336")  # red
                        
                        if is_hit_marked or is_fault_marked:
                            student_markings.append({
                                'frame_idx': frame_idx,
                                'is_hit': is_hit_marked,
                                'is_fault': is_fault_marked
                            })
                
                # Validate student markings
                if len(student_markings) == 0:
                    errors.append(f"Page {page_id} (column {page_idx + 1}): No marking found - should be {'hit' if expected_is_hit else 'fault'} in frame {expected_frame_idx}")
                elif len(student_markings) > 1:
                    errors.append(f"Page {page_id} (column {page_idx + 1}): Multiple markings found - should have only one {'hit' if expected_is_hit else 'fault'}")
                else:
                    # Exactly one marking - check if it's correct
                    marking = student_markings[0]
                    student_frame_idx = marking['frame_idx']
                    student_is_hit = marking['is_hit']
                    
                    # Check frame location and hit/fault type
                    if student_frame_idx == expected_frame_idx and student_is_hit == expected_is_hit:
                        correct_count += 1
                    else:
                        expected_type = "hit" if expected_is_hit else "fault"
                        student_type = "hit" if student_is_hit else "fault"
                        if student_frame_idx != expected_frame_idx:
                            errors.append(f"Page {page_id} (column {page_idx + 1}): Wrong frame location - expected frame {expected_frame_idx}, marked in frame {student_frame_idx}")
                        if student_is_hit != expected_is_hit:
                            errors.append(f"Page {page_id} (column {page_idx + 1}): Wrong type - expected {expected_type}, marked as {student_type}")
                            
        # Display results
        accuracy = (correct_count / total_checks * 100) if total_checks > 0 else 0
        
        if not errors:
            result_text = "<b>✓ Perfect solution!</b><br><br>"
        else:
            result_text = f"<b>Solution check complete</b><br>Accuracy: {accuracy:.1f}%<br><br>"
            if len(errors) <= 10:
                result_text += "<b>Issues found:</b><br>" + "<br>".join(errors[:10])
            else:
                result_text += f"<b>Issues found ({len(errors)} total, showing first 10):</b><br>" + "<br>".join(errors[:10])
                
        # Add statistics
        result_text += f"<br><br><b>Correct Solution Statistics:</b><br>"
        result_text += f"Total Page Accesses: {len(self.solution_result.accesses)}<br>"
        result_text += f"Page Hits: {self.solution_result.page_hits}<br>"
        result_text += f"Page Faults: {self.solution_result.page_faults}<br>"
        result_text += f"Hit Ratio: {self.solution_result.get_hit_ratio():.2%}<br>"
        
        self.results_label.setText(result_text)
        
    def show_solution(self):
        """Show the correct solution."""
        self.read_frame_table()
        
        if not self.page_sequence or not self.frames:
            QMessageBox.warning(self, "No Data", "Please enter page sequence and frame data.")
            return
            
        # Get the selected algorithm
        algorithm_name = self.algorithm_combo.currentText()
        algorithm = self.algorithms[algorithm_name]
        
        # Calculate correct solution using frame data
        if hasattr(algorithm, 'replace_pages_with_frames'):
            self.solution_result = algorithm.replace_pages_with_frames(self.page_sequence, self.frames)
        else:
            self.solution_result = algorithm.replace_pages(self.page_sequence, len(self.frames))
        
        # Fill the table with correct solution
        self.fill_solution_table()
        
        # Lock the table
        self.is_locked = True
        self.lock_table_cells()
        
        # Update results display
        self.update_results_display()
        
    def fill_solution_table(self):
        """Fill the solution table with correct solution."""
        if not self.solution_result:
            return
            
        # Clear and fill with correct data
        for access_idx, access in enumerate(self.solution_result.accesses):
            col_idx = access_idx + 3  # Offset by 3 for Frame ID, Load Time, Page in Memory
            
            for frame_idx in range(len(self.frames)):
                if frame_idx < len(access.frames_state):
                    page = access.frames_state[frame_idx]
                    item = self.solution_table.item(frame_idx, col_idx)
                    
                    if item:
                        if page:
                            item.setText(page)
                            # Color code based on whether this page was accessed and hit/fault
                            if page == access.page_id:
                                if access.is_hit:
                                    item.setBackground(QColor("#4caf50"))  # Green for hit
                                else:
                                    item.setBackground(QColor("#f44336"))  # Red for fault
                                item.setForeground(QColor("white"))
                            else:
                                item.setBackground(QColor("white"))
                                item.setForeground(QColor("black"))
                        else:
                            item.setText("")
                            item.setBackground(QColor("white"))
                            item.setForeground(QColor("black"))
                            
    def lock_table_cells(self):
        """Lock all table cells to prevent editing."""
        for row in range(len(self.frames)):
            for col in range(3, self.solution_table.columnCount()):  # Start at column 3 (page columns)
                item = self.solution_table.item(row, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    
    def update_results_display(self):
        """Update the results display with algorithm statistics."""
        if not self.solution_result:
            return
            
        hit_ratio = self.solution_result.get_hit_ratio()
        fault_ratio = self.solution_result.get_fault_ratio()
        
        results_text = f"""
<b>Page Replacement Results:</b><br>
<br>
<b>Algorithm:</b> {self.algorithm_combo.currentText()}<br>
<b>Page Sequence:</b> {', '.join(self.solution_result.page_sequence)}<br>
<b>Number of Frames:</b> {self.solution_result.num_frames}<br>
<br>
<b>Statistics:</b><br>
• Total Page Accesses: {len(self.solution_result.accesses)}<br>
• Page Hits: {self.solution_result.page_hits}<br>
• Page Faults: {self.solution_result.page_faults}<br>
• Hit Ratio: {hit_ratio:.2%}<br>
• Fault Ratio: {fault_ratio:.2%}<br>
        """
        
        self.results_label.setText(results_text.strip())
        
    def reset_solution(self):
        """Reset the solution table and unlock cells."""
        self.is_locked = False
        self.solution_result = None
        self.results_label.setText("")
        
        # Clear solution cells and unlock them
        if self.frames and self.page_sequence:
            for row in range(len(self.frames)):
                for col in range(3, self.solution_table.columnCount()):  # Start at column 3 (page columns)
                    item = self.solution_table.item(row, col)
                    if item:
                        item.setText("")
                        item.setBackground(QColor("white"))
                        item.setForeground(QColor("black"))
                        item.setFlags(item.flags() | Qt.ItemIsEditable)
