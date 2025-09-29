"""Interactive main window for Page Replacement Algorithms practice."""

import sys
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
import random

import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import PRA algorithms and models
from algorithms.fifo import FIFOReplacer
from algorithms.base_replacer import PageReplacementResult
from models.frame import Frame


class DraggableFrameBlock(QLabel):
    """Draggable frame block for queue visualization."""
    
    def __init__(self, frame_id: str, parent=None):
        super().__init__(parent)
        self.frame_id = frame_id
        self.setText(f"F{frame_id}")
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(40, 30)
        self.setStyleSheet("""
            QLabel {
                background-color: #4a90e2;
                color: white;
                border: 2px solid #357abd;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QLabel:hover {
                background-color: #5ba0f2;
            }
        """)
        
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
        
        # Create drag pixmap
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        
        # Execute drag
        drag.exec(Qt.MoveAction)


class QueueVisualizationWidget(QWidget):
    """Widget for visualizing and managing the FIFO queue order."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.frame_blocks = []
        self.init_ui()
        
    def init_ui(self):
        """Initialize the queue visualization UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("FIFO Queue Order:")
        title.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(title)
        
        # Queue container
        self.queue_container = QWidget()
        self.queue_layout = QHBoxLayout(self.queue_container)
        self.queue_layout.setSpacing(5)
        self.queue_layout.setContentsMargins(10, 5, 10, 5)
        
        # Style the container
        self.queue_container.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 2px dashed #ccc;
                border-radius: 5px;
                min-height: 50px;
            }
        """)
        self.queue_container.setAcceptDrops(True)
        self.queue_container.dragEnterEvent = self.drag_enter_event
        self.queue_container.dragMoveEvent = self.drag_move_event
        self.queue_container.dropEvent = self.drop_event
        
        layout.addWidget(self.queue_container)
        
        # Instructions
        instructions = QLabel("Drag frames to reorder queue (left = oldest, right = newest)")
        instructions.setStyleSheet("color: #666; font-size: 10px; margin-top: 5px;")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
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
            self.frame_blocks.append(block)
            self.queue_layout.addWidget(block)
            
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
                    
                    # Insert at new position
                    self.queue_layout.insertWidget(insert_index, dragged_block)
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


class PRAMainWindow(QWidget):
    """Interactive main window for Page Replacement Algorithms practice."""
    
    def __init__(self):
        super().__init__()
        self.frames: List[Frame] = []
        self.page_sequence: List[str] = []
        self.frame_table: Optional[QTableWidget] = None
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
            "FIFO": FIFOReplacer()
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
        self.algorithm_combo.currentTextChanged.connect(self.on_algorithm_changed)
        controls_layout.addWidget(QLabel("Algorithm:"))
        controls_layout.addWidget(self.algorithm_combo)
        
        # Page sequence input
        self.page_input = QLineEdit()
        self.page_input.setPlaceholderText("Enter page sequence (e.g., 7,0,1,2,0,3,0,4)")
        self.page_input.textChanged.connect(self.on_page_sequence_changed)
        controls_layout.addWidget(QLabel("Pages:"))
        controls_layout.addWidget(self.page_input)
        
        # Control buttons
        check_btn = QPushButton("Check Solution")
        check_btn.clicked.connect(self.check_solution)
        controls_layout.addWidget(check_btn)
        
        show_btn = QPushButton("Show Solution")
        show_btn.clicked.connect(self.show_solution)
        controls_layout.addWidget(show_btn)
        
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_solution)
        controls_layout.addWidget(reset_btn)
        
        # Algorithm name display
        self.algorithm_name_label = QLabel("Current Algorithm: FIFO")
        self.algorithm_name_label.setStyleSheet("""
            QLabel {
                font-family: Arial;
                font-size: 14px;
                font-weight: bold;
                color: white;
                background: transparent;
                border: none;
                padding: 8px;
            }
        """)
        controls_layout.addWidget(self.algorithm_name_label)
        
        controls_layout.addStretch()
        main_layout.addLayout(controls_layout)
        
        # Main content layout
        content_layout = QHBoxLayout()
        
        # Left panel - Frame input table
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Frame Input:"))
        
        self.setup_frame_table()
        left_panel.addWidget(self.frame_table)
        
        # Frame control buttons
        frame_controls = QHBoxLayout()
        add_frame_btn = QPushButton("Add Frame")
        add_frame_btn.clicked.connect(self.add_frame)
        delete_frame_btn = QPushButton("Delete Frame")
        delete_frame_btn.clicked.connect(self.delete_frame)
        randomize_btn = QPushButton("Randomize")
        randomize_btn.clicked.connect(self.generate_random_problem)
        
        frame_controls.addWidget(add_frame_btn)
        frame_controls.addWidget(delete_frame_btn)
        frame_controls.addWidget(randomize_btn)
        left_panel.addLayout(frame_controls)
        
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        left_widget.setFixedWidth(400)  # Increased width for frame data
        content_layout.addWidget(left_widget)
        
        # Right panel - Solution table
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("Solution Grid:"))
        
        self.setup_solution_table()
        right_panel.addWidget(self.solution_table)
        
        # Queue visualization widget
        self.queue_widget = QueueVisualizationWidget()
        right_panel.addWidget(self.queue_widget)
        
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
        
        right_panel.addWidget(self.results_scroll_area)
        
        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        content_layout.addWidget(right_widget)
        
        main_layout.addLayout(content_layout)
        
    def setup_frame_table(self):
        """Set up the frame input table."""
        self.frame_table = QTableWidget(0, 3)
        self.frame_table.setHorizontalHeaderLabels(["Frame ID", "Load Time", "Page in Memory"])
        self.frame_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Connect signal to update solution table when frame data changes
        self.frame_table.itemChanged.connect(self.on_frame_table_changed)
        
    def setup_solution_table(self):
        """Set up the solution grid for visualization."""
        self.solution_table = QTableWidget(0, 0)
        self.solution_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.solution_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.solution_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.solution_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Connect cell events
        self.solution_table.cellClicked.connect(self.on_cell_clicked)
        self.solution_table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        
        # Enable context menu
        self.solution_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.solution_table.customContextMenuRequested.connect(self.show_context_menu)
        
        # Set row height and column width
        self.solution_table.verticalHeader().setDefaultSectionSize(30)
        
    def add_sample_frames(self):
        """Add sample frames for demonstration."""
        sample_frames = [
            Frame("3", 11, "5"),
            Frame("2", 8, "8"),
            Frame("1", 3, "1"),
            Frame("0", 14, "4"),
        ]
        self.frames = sample_frames
        self.update_frame_table()
        
        # Set sample page sequence (using 1-15 range)
        self.page_input.setText("7,1,2,3,1,4,1,5,2,3,1,3,2,1,2,1")
        self.parse_page_sequence("7,1,2,3,1,4,1,5,2,3,1,3,2,1,2,1")
        
    def update_frame_table(self):
        """Update the frame table with current frames."""
        self.frame_table.setRowCount(len(self.frames))
        for i, frame in enumerate(self.frames):
            self.frame_table.setItem(i, 0, QTableWidgetItem(frame.frame_id))
            self.frame_table.setItem(i, 1, QTableWidgetItem(str(frame.load_time)))
            self.frame_table.setItem(i, 2, QTableWidgetItem(frame.pages_in_memory))
        
        # Update queue visualization
        if self.queue_widget:
            self.queue_widget.update_frames(self.frames)
    
    def on_frame_table_changed(self, item):
        """Handle when frame table data is edited by user."""
        # Read the updated frame data and refresh solution table
        self.read_frame_table()
        self.update_solution_table()
        
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
        """Read frame data from the table."""
        self.frames = []
        for i in range(self.frame_table.rowCount()):
            frame_id_item = self.frame_table.item(i, 0)
            load_time_item = self.frame_table.item(i, 1)
            pages_item = self.frame_table.item(i, 2)
            
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
        if self.algorithm_name_label:
            self.algorithm_name_label.setText(f"Current Algorithm: {algorithm}")
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
        num_cols = num_pages + 2   # pages + Frame ID + Load time columns
        
        self.solution_table.setRowCount(num_rows)
        self.solution_table.setColumnCount(num_cols)
        
        # Set up headers
        headers = ["Frame ID", "Page in Memory"] + self.page_sequence
        self.solution_table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        self.solution_table.setColumnWidth(0, 80)  # Frame ID column
        self.solution_table.setColumnWidth(1, 120)  # Page in Memory column
        for i in range(2, num_cols):
            self.solution_table.setColumnWidth(i, 30)  # Page columns
            
        # Fill initial data
        self.fill_solution_table_structure()
        
    def fill_solution_table_structure(self):
        """Fill the basic structure of the solution table."""
        if not self.frames:
            return
            
        # Clear existing data
        for row in range(self.solution_table.rowCount()):
            for col in range(self.solution_table.columnCount()):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignCenter)
                self.solution_table.setItem(row, col, item)
                
        # Frame rows
        for frame_idx, frame in enumerate(self.frames):
            # Frame ID column
            frame_item = QTableWidgetItem(frame.frame_id)
            frame_item.setFlags(frame_item.flags() & ~Qt.ItemIsEditable)
            frame_item.setTextAlignment(Qt.AlignCenter)
            self.solution_table.setItem(frame_idx, 0, frame_item)
            
            # Page in Memory column
            page_item = QTableWidgetItem(frame.pages_in_memory)
            page_item.setFlags(page_item.flags() & ~Qt.ItemIsEditable)
            page_item.setTextAlignment(Qt.AlignCenter)
            self.solution_table.setItem(frame_idx, 1, page_item)
            
            # Page columns - these are interactive
            for page_idx in range(len(self.page_sequence)):
                col_idx = page_idx + 2
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
        self.solution_table.setItem(algorithm_row, 1, alg_name_item)
        
        # Legend row
        legend_row = len(self.frames) + 1
        legend_label_item = QTableWidgetItem("Legend:")
        legend_label_item.setFlags(legend_label_item.flags() & ~Qt.ItemIsEditable)
        legend_label_item.setTextAlignment(Qt.AlignCenter)
        self.solution_table.setItem(legend_row, 0, legend_label_item)
        
        # Add legend items
        if self.solution_table.columnCount() > 2:
            hit_item = QTableWidgetItem("Hit")
            hit_item.setFlags(hit_item.flags() & ~Qt.ItemIsEditable)
            hit_item.setTextAlignment(Qt.AlignCenter)
            hit_item.setBackground(QColor("#4caf50"))
            hit_item.setForeground(QColor("white"))
            self.solution_table.setItem(legend_row, 2, hit_item)
            
        if self.solution_table.columnCount() > 3:
            fault_item = QTableWidgetItem("Fault")
            fault_item.setFlags(fault_item.flags() & ~Qt.ItemIsEditable)
            fault_item.setTextAlignment(Qt.AlignCenter)
            fault_item.setBackground(QColor("#f44336"))
            fault_item.setForeground(QColor("white"))
            self.solution_table.setItem(legend_row, 3, fault_item)
            
    def on_cell_clicked(self, row: int, col: int):
        """Handle cell click events."""
        if col < 2 or self.is_locked:  # Skip Frame ID and Load time columns
            return
            
        if row >= len(self.frames):  # Skip algorithm and legend rows
            return
            
        item = self.solution_table.item(row, col)
        if item is None:
            return
            
        # Get the page that should be in this cell
        page_idx = col - 2
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
        if col < 2 or self.is_locked or row >= len(self.frames):
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
        
        if col < 2 or row >= len(self.frames):
            return
            
        menu = QMenu(self)
        
        # Add page action
        page_idx = col - 2
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
            col_idx = page_idx + 2
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
                col_idx = page_idx + 2
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
            col_idx = access_idx + 2
            
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
            for col in range(2, self.solution_table.columnCount()):
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
                for col in range(2, self.solution_table.columnCount()):
                    item = self.solution_table.item(row, col)
                    if item:
                        item.setText("")
                        item.setBackground(QColor("white"))
                        item.setForeground(QColor("black"))
                        item.setFlags(item.flags() | Qt.ItemIsEditable)
