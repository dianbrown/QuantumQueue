"""
PRA Clock Tutorial Page - Step-by-step walkthrough of Clock Page Replacement Algorithm
Features R-bit visualization and pointer/arrow indicator for clock hand position
Uses a fixed circular frame order with visual pointer movement
"""

import json
import os
import random
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                              QLabel, QTableWidget, QTableWidgetItem, QFrame,
                              QScrollArea, QHeaderView, QLineEdit, QSpinBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor


class ClockBlockWidget(QFrame):
    """Visual block representing a frame in the clock with R-bit and pointer indicator"""
    
    def __init__(self, frame_id: str, r_bit: int = 1, is_pointer: bool = False, parent=None):
        super().__init__(parent)
        self.frame_id = frame_id
        self.r_bit = r_bit
        self.is_pointer = is_pointer
        self.theme_colors = {}
        
        self.setup_ui()
        self.update_display()
    
    def setup_ui(self):
        """Setup the block UI with pointer arrow"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(0)
        
        # Pointer arrow (above the block)
        self.pointer_label = QLabel("▼")
        self.pointer_label.setAlignment(Qt.AlignCenter)
        self.pointer_label.setFixedHeight(18)
        layout.addWidget(self.pointer_label)
        
        # Frame content label
        self.content_label = QLabel()
        self.content_label.setAlignment(Qt.AlignCenter)
        self.content_label.setFixedSize(50, 35)
        layout.addWidget(self.content_label)
        
        self.setFixedSize(56, 60)
    
    def set_r_bit(self, r_bit: int):
        """Update the R-bit value and refresh display"""
        self.r_bit = r_bit
        self.update_display()
    
    def set_pointer(self, is_pointer: bool):
        """Update whether this block has the pointer"""
        self.is_pointer = is_pointer
        self.update_display()
    
    def set_theme_colors(self, theme_colors: dict):
        """Set theme colors for the block."""
        self.theme_colors = theme_colors
        self.update_display()
    
    def update_display(self):
        """Update the text display with R-bit and pointer"""
        self.content_label.setText(f"F{self.frame_id}\nR:{self.r_bit}")
        
        # Show/hide pointer arrow
        if self.is_pointer:
            pointer_color = self.theme_colors.get('pointer_color', '#ff5722')
            self.pointer_label.setStyleSheet(f"""
                QLabel {{
                    color: {pointer_color};
                    font-size: 16px;
                    font-weight: bold;
                    background-color: transparent;
                }}
            """)
            self.pointer_label.setText("▼")
        else:
            self.pointer_label.setStyleSheet("QLabel { color: transparent; background-color: transparent; }")
            self.pointer_label.setText("")
        
        self.update_content_style()
    
    def update_content_style(self):
        """Update the content label stylesheet based on R-bit value."""
        if self.r_bit == 1:
            # R-bit = 1: Recently used (blue/primary)
            bg_color = self.theme_colors.get('queue_block_bg', '#4a90e2')
            border_color = self.theme_colors.get('queue_block_border', '#357abd')
        else:
            # R-bit = 0: Not recently used (orange/warning)
            bg_color = self.theme_colors.get('rbit_zero_bg', '#ff9800')
            border_color = self.theme_colors.get('rbit_zero_border', '#f57c00')
        
        text_color = self.theme_colors.get('queue_block_text', 'white')
        
        self.content_label.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border: 2px solid {border_color};
                border-radius: 3px;
                font-weight: bold;
                font-size: 11px;
            }}
        """)


class ClockTutorialPage(QWidget):
    """Step-by-step Clock Page Replacement Algorithm tutorial"""
    
    back_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_step = 0
        self.current_theme = {}
        self.hit_color = QColor("#4caf50")  # Green for hits
        self.fault_color = QColor("#f44336")  # Red for faults
        
        # Frame and page data
        self.frames = []  # List of dicts: {id, load_time, page}
        self.page_sequence = []
        self.steps = []
        self.clock_blocks = []  # Visual clock blocks
        
        self._updating_table = False
        self.step_templates = self._load_step_templates()
        
        self.setup_ui()
        self._generate_random_problem()
        self._setup_unified_table()
        self._generate_steps()
        self._show_step(0)
    
    def _load_step_templates(self):
        """Load step description templates from JSON file"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '..', 'tutorial_kb', 'clock_steps.json'),
            'tutorial_kb/clock_steps.json',
        ]
        for path in possible_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                continue
        return {"step_types": {}}
    
    def _generate_random_problem(self):
        """Generate random frame data and page sequence"""
        num_frames = 5  # Fixed at 5 frames
        
        self.frames = []
        
        # Generate unique load times (1-20, no duplicates)
        available_load_times = list(range(1, 21))
        random.shuffle(available_load_times)
        selected_load_times = available_load_times[:num_frames]
        
        # Generate frames with descending IDs
        used_pages = set()
        for i in range(num_frames):
            frame_id = str(num_frames - 1 - i)
            load_time = selected_load_times[i]
            
            # Generate unique page for initial state (1-15)
            page = random.randint(1, 15)
            while page in used_pages:
                page = random.randint(1, 15)
            used_pages.add(page)
            
            self.frames.append({
                "id": frame_id,
                "load_time": load_time,
                "page": str(page)
            })
        
        # Generate random page sequence (8-16 pages for tutorial brevity)
        sequence_length = random.randint(8, 16)
        self.page_sequence = []
        
        for _ in range(sequence_length):
            page = random.randint(1, 15)
            self.page_sequence.append(str(page))
    
    def _get_clock_order(self):
        """Get the fixed clock order: highest frame ID first, then ascending,
        rotated to start at the frame with oldest load time (pointer position).
        
        This matches Algorithm Rules: 
        - Order: Highest frame first, then ascending (e.g., 4→0→1→2→3)
        - Initial pointer: Points to frame with oldest load time
        """
        if not self.frames:
            return []
        
        # Get all frame IDs and sort numerically
        frame_ids = [f["id"] for f in self.frames]
        frame_ids_sorted = sorted(frame_ids, key=lambda x: int(x) if x.isdigit() else 0)
        
        # Create circular order: [highest, 0, 1, 2, ..., highest-1]
        if frame_ids_sorted:
            highest = frame_ids_sorted[-1]  # Highest ID
            rest = frame_ids_sorted[:-1]  # All others in ascending order
            circular_order = [highest] + rest
            
            # Find the frame with oldest load time and rotate to start there
            oldest_frame = min(self.frames, key=lambda f: f["load_time"])
            oldest_frame_id = oldest_frame["id"]
            
            if oldest_frame_id in circular_order:
                pointer_index = circular_order.index(oldest_frame_id)
                # Rotate the circular order to start at the pointer
                rotated_order = circular_order[pointer_index:] + circular_order[:pointer_index]
                return rotated_order
            
            return circular_order
        
        return frame_ids
    
    def _get_initial_pointer(self, clock_order):
        """Get initial pointer position (always 0 since we rotated the order to start at oldest)"""
        return 0 if clock_order else -1
    
    def _get_data_from_table(self):
        """Read frame data from unified table"""
        self.frames = []
        for row in range(5):  # Fixed 5 frames
            try:
                frame_id = self.unified_table.item(row, 0).text() if self.unified_table.item(row, 0) else str(row)
                load_time = int(self.unified_table.item(row, 1).text()) if self.unified_table.item(row, 1) else 1
                page = self.unified_table.item(row, 2).text() if self.unified_table.item(row, 2) else "1"
                
                load_time = max(1, min(30, load_time))
                
                self.frames.append({
                    "id": frame_id,
                    "load_time": load_time,
                    "page": page
                })
            except (ValueError, AttributeError):
                self.frames.append({"id": str(row), "load_time": 1, "page": "1"})
        
        # Parse page sequence from input
        seq_text = self.page_input.text().strip()
        if seq_text:
            self.page_sequence = [p.strip() for p in seq_text.split(',') if p.strip()]
        else:
            self.page_sequence = []
    
    def _on_table_cell_changed(self, row, column):
        """Handle cell value changes in the unified table"""
        if self._updating_table:
            return
        # Only react to changes in editable columns (1: Load Time, 2: Page in Memory)
        if column < 1 or column > 2:
            return
        
        self._get_data_from_table()
        self._rebuild_table_columns()
        self._generate_steps()
        self.current_step = 0
        self._show_step(0)
    
    def _on_page_sequence_changed(self):
        """Handle page sequence input changes"""
        self._get_data_from_table()
        self._rebuild_table_columns()
        self._generate_steps()
        self.current_step = 0
        self._show_step(0)
    
    def _generate_steps(self):
        """Generate tutorial steps dynamically based on current data"""
        self.steps = []
        templates = self.step_templates.get("step_types", {})
        
        if not self.frames or not self.page_sequence:
            return
        
        # Get clock order (fixed circular order)
        clock_order = self._get_clock_order()
        pointer_index = self._get_initial_pointer(clock_order)
        
        # Current memory state: frame_id -> page
        frame_state = {f["id"]: f["page"] for f in self.frames}
        
        # R-bit state: frame_id -> R-bit (0 or 1)
        r_bits = {f["id"]: 1 for f in self.frames}  # All start with R-bit = 1
        
        # Track which pages are in memory (for hit/fault determination)
        pages_in_memory = {f["page"] for f in self.frames}
        
        # Track if first fault
        first_fault = True
        
        # Helper function to format R-bit values
        def format_rbits(r_bits, clock_order):
            return ", ".join([f"F{fid}:R{r_bits[fid]}" for fid in clock_order])
        
        # Generate initial step
        clock_order_str = " -> ".join([f"F{fid}" for fid in clock_order])
        frame_list = ", ".join([f"F{f['id']}={f['page']}" for f in self.frames])
        
        initial_tmpl = templates.get("initial", {})
        self.steps.append({
            "title": initial_tmpl.get("title", "Step 0: Initial State"),
            "description": initial_tmpl.get("description", "").format(
                num_frames=len(self.frames),
                frame_list=frame_list
            ),
            "solution_grid": {},
            "clock_order": [],
            "frame_state": frame_state.copy(),
            "r_bits": r_bits.copy(),
            "pointer_index": -1  # No pointer shown in initial state
        })
        
        # Step 1: Establish Clock Order
        order_tmpl = templates.get("order_frames", {})
        self.steps.append({
            "title": order_tmpl.get("title", "Step 1: Establish Clock Order"),
            "description": order_tmpl.get("description", "").format(
                clock_order=clock_order_str,
                pointer_frame=clock_order[pointer_index],
                rbit_values=format_rbits(r_bits, clock_order)
            ),
            "solution_grid": {},
            "clock_order": clock_order.copy(),
            "frame_state": frame_state.copy(),
            "r_bits": r_bits.copy(),
            "pointer_index": pointer_index
        })
        
        # Process each page request
        solution_grid = {}  # (frame_id, col_idx) -> {text, is_hit}
        page_hits = 0
        page_faults = 0
        step_num = 2
        
        for col_idx, requested_page in enumerate(self.page_sequence):
            # Check if page is in memory
            if requested_page in pages_in_memory:
                # HIT - find which frame has this page
                hit_frame = None
                for fid, page in frame_state.items():
                    if page == requested_page:
                        hit_frame = fid
                        break
                
                # Set R-bit to 1 on hit
                r_bits[hit_frame] = 1
                
                page_hits += 1
                solution_grid[(hit_frame, col_idx)] = {"text": requested_page, "is_hit": True}
                
                hit_tmpl = templates.get("page_hit", {})
                self.steps.append({
                    "title": hit_tmpl.get("title", f"Step {step_num}: HIT").format(
                        step=step_num, page=requested_page
                    ),
                    "description": hit_tmpl.get("description", "").format(
                        step=step_num, page=requested_page, frame_id=hit_frame,
                        pointer_frame=clock_order[pointer_index],
                        rbit_values=format_rbits(r_bits, clock_order)
                    ),
                    "solution_grid": {k: v.copy() for k, v in solution_grid.items()},
                    "clock_order": clock_order.copy(),
                    "frame_state": frame_state.copy(),
                    "r_bits": r_bits.copy(),
                    "pointer_index": pointer_index
                })
            else:
                # FAULT - use Clock algorithm
                page_faults += 1
                
                sweep_log = []
                victim_index = pointer_index
                
                # Check if all R-bits are 1 or first fault
                all_rbits_one = all(r_bits[fid] == 1 for fid in clock_order) or first_fault
                
                if all_rbits_one:
                    # Reset all R-bits to 0
                    for fid in clock_order:
                        r_bits[fid] = 0
                    first_fault = False
                    # Victim is at pointer
                    victim_index = pointer_index
                    fault_tmpl = templates.get("page_fault_all_rbits_one", {})
                else:
                    # Sweep to find victim
                    while r_bits[clock_order[victim_index]] == 1:
                        sweep_log.append(f"- Frame {clock_order[victim_index]}: R-bit=1 -> Set to 0, advance pointer")
                        r_bits[clock_order[victim_index]] = 0
                        victim_index = (victim_index + 1) % len(clock_order)
                    
                    if sweep_log:
                        fault_tmpl = templates.get("page_fault_sweep", {})
                    else:
                        fault_tmpl = templates.get("page_fault_direct", {})
                
                victim_frame = clock_order[victim_index]
                old_page = frame_state[victim_frame]
                
                # Perform replacement
                pages_in_memory.discard(old_page)
                pages_in_memory.add(requested_page)
                frame_state[victim_frame] = requested_page
                
                # Set new page's R-bit to 1
                r_bits[victim_frame] = 1
                
                # Advance pointer
                pointer_index = (victim_index + 1) % len(clock_order)
                
                solution_grid[(victim_frame, col_idx)] = {"text": requested_page, "is_hit": False}
                
                description_kwargs = {
                    "step": step_num,
                    "page": requested_page,
                    "victim_frame": victim_frame,
                    "old_page": old_page,
                    "new_pointer_frame": clock_order[pointer_index],
                    "rbit_values": format_rbits(r_bits, clock_order),
                    "sweep_log": "\n".join(sweep_log) if sweep_log else ""
                }
                
                self.steps.append({
                    "title": fault_tmpl.get("title", f"Step {step_num}: FAULT").format(
                        step=step_num, page=requested_page
                    ),
                    "description": fault_tmpl.get("description", "").format(**description_kwargs),
                    "solution_grid": {k: v.copy() for k, v in solution_grid.items()},
                    "clock_order": clock_order.copy(),
                    "frame_state": frame_state.copy(),
                    "r_bits": r_bits.copy(),
                    "pointer_index": pointer_index
                })
            
            step_num += 1
        
        # Final step with statistics
        total_requests = len(self.page_sequence)
        hit_ratio = f"{(page_hits / total_requests * 100):.1f}%" if total_requests > 0 else "0%"
        fault_ratio = f"{(page_faults / total_requests * 100):.1f}%" if total_requests > 0 else "0%"
        
        frame_contents = "\n".join([f"- Frame {fid}: Page {page}" for fid, page in frame_state.items()])
        rbit_summary = "\n".join([f"- Frame {fid}: R-bit = {r_bits[fid]}" for fid in clock_order])
        
        final_tmpl = templates.get("final", {})
        self.steps.append({
            "title": final_tmpl.get("title", "Final Results").format(step=step_num),
            "description": final_tmpl.get("description", "").format(
                step=step_num,
                frame_contents=frame_contents,
                rbit_summary=rbit_summary,
                pointer_frame=clock_order[pointer_index],
                total_requests=total_requests,
                page_hits=page_hits,
                page_faults=page_faults,
                hit_ratio=hit_ratio,
                fault_ratio=fault_ratio
            ),
            "solution_grid": {k: v.copy() for k, v in solution_grid.items()},
            "clock_order": clock_order.copy(),
            "frame_state": frame_state.copy(),
            "r_bits": r_bits.copy(),
            "pointer_index": pointer_index
        })
        
        if hasattr(self, 'step_indicator'):
            self.step_indicator.setText(f"Step 0 of {len(self.steps) - 1}")
    
    def setup_ui(self):
        """Setup the tutorial UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Top row: Back button and Generate Random button
        top_layout = QHBoxLayout()
        
        self.back_btn = QPushButton("Back to Help")
        self.back_btn.setObjectName("backBtn")
        self.back_btn.setMaximumWidth(150)
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.clicked.connect(self.back_requested.emit)
        top_layout.addWidget(self.back_btn)
        
        top_layout.addStretch()
        
        self.random_btn = QPushButton("Generate Random")
        self.random_btn.setObjectName("randomBtn")
        self.random_btn.setCursor(Qt.PointingHandCursor)
        self.random_btn.clicked.connect(self._on_random_clicked)
        top_layout.addWidget(self.random_btn)
        
        layout.addLayout(top_layout)
        
        # Title
        self.page_title = QLabel("Clock Page Replacement Tutorial")
        self.page_title.setObjectName("tutorialTitle")
        layout.addWidget(self.page_title)
        
        # Page sequence input (above the unified table)
        page_seq_layout = QHBoxLayout()
        page_seq_label = QLabel("Page Sequence:")
        page_seq_label.setObjectName("sectionLabel")
        page_seq_layout.addWidget(page_seq_label)
        
        self.page_input = QLineEdit()
        self.page_input.setPlaceholderText("Enter page sequence (e.g., 7,0,1,2,0,3)")
        self.page_input.textChanged.connect(self._on_page_sequence_changed)
        page_seq_layout.addWidget(self.page_input)
        layout.addLayout(page_seq_layout)
        
        # Unified table (Frame ID, Load Time, Page in Memory, then page sequence columns)
        self.unified_table = QTableWidget(5, 3)  # Start with 5 rows, 3 columns
        self.unified_table.setHorizontalHeaderLabels(["Frame ID", "Load Time", "Page in Memory"])
        self.unified_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.unified_table.setMaximumHeight(200)
        self.unified_table.verticalHeader().hide()
        self.unified_table.cellChanged.connect(self._on_table_cell_changed)
        layout.addWidget(self.unified_table)
        
        # Clock visualization section
        clock_section = QWidget()
        clock_layout = QVBoxLayout(clock_section)
        clock_layout.setContentsMargins(0, 10, 0, 10)
        
        # Clock label
        clock_header = QHBoxLayout()
        self.clock_label = QLabel("Clock Order (Fixed Circular: Highest → 0 → 1 → ...):")
        self.clock_label.setObjectName("sectionLabel")
        clock_header.addWidget(self.clock_label)
        
        clock_header.addStretch()
        
        clock_layout.addLayout(clock_header)
        
        self.clock_container = QWidget()
        self.clock_container_layout = QHBoxLayout(self.clock_container)
        self.clock_container_layout.setSpacing(8)
        self.clock_container_layout.setContentsMargins(10, 10, 10, 10)
        self.clock_container_layout.setAlignment(Qt.AlignLeft)
        clock_layout.addWidget(self.clock_container)
        
        layout.addWidget(clock_section)
        
        # Step info section
        step_frame = QFrame()
        step_frame.setObjectName("stepFrame")
        step_layout = QVBoxLayout(step_frame)
        step_layout.setSpacing(5)
        step_layout.setContentsMargins(15, 15, 15, 15)
        
        self.step_title = QLabel("Step 0: Initial State")
        self.step_title.setObjectName("stepTitle")
        step_layout.addWidget(self.step_title)
        
        # Scroll area for description
        desc_scroll = QScrollArea()
        desc_scroll.setWidgetResizable(True)
        desc_scroll.setMinimumHeight(120)
        desc_scroll.setMaximumHeight(180)
        desc_scroll.setObjectName("descriptionScroll")
        
        self.step_description = QLabel("")
        self.step_description.setObjectName("stepDescription")
        self.step_description.setWordWrap(True)
        self.step_description.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        desc_scroll.setWidget(self.step_description)
        step_layout.addWidget(desc_scroll)
        
        step_layout.addStretch(0)  # Prevent expansion
        
        layout.addWidget(step_frame)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        nav_layout.addStretch()
        
        self.prev_btn = QPushButton("Previous")
        self.prev_btn.setObjectName("navBtn")
        self.prev_btn.setCursor(Qt.PointingHandCursor)
        self.prev_btn.clicked.connect(self._prev_step)
        nav_layout.addWidget(self.prev_btn)
        
        self.step_indicator = QLabel("Step 0 of 0")
        self.step_indicator.setObjectName("stepIndicator")
        nav_layout.addWidget(self.step_indicator)
        
        self.next_btn = QPushButton("Next")
        self.next_btn.setObjectName("navBtn")
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.clicked.connect(self._next_step)
        nav_layout.addWidget(self.next_btn)
        
        nav_layout.addStretch()
        layout.addLayout(nav_layout)
    
    def _setup_unified_table(self):
        """Setup the unified table with frame data and page sequence columns"""
        self._updating_table = True
        
        if not self.frames:
            self.unified_table.setRowCount(0)
            self.unified_table.setColumnCount(3)
            self._updating_table = False
            return
        
        num_frames = len(self.frames)
        num_pages = len(self.page_sequence) if self.page_sequence else 0
        
        # Columns: Frame ID, Load Time, Page in Memory, then page request columns
        total_columns = 3 + num_pages
        self.unified_table.setRowCount(num_frames)
        self.unified_table.setColumnCount(total_columns)
        
        # Headers
        headers = ["Frame ID", "Load Time", "Page in Memory"] + self.page_sequence
        self.unified_table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        self.unified_table.setColumnWidth(0, 70)
        self.unified_table.setColumnWidth(1, 75)
        self.unified_table.setColumnWidth(2, 120)
        for i in range(3, total_columns):
            self.unified_table.setColumnWidth(i, 40)
        
        # Fill initial structure
        for row, frame in enumerate(self.frames):
            # Frame ID (read-only)
            id_item = QTableWidgetItem(frame["id"])
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            id_item.setTextAlignment(Qt.AlignCenter)
            self.unified_table.setItem(row, 0, id_item)
            
            # Load Time (editable)
            load_item = QTableWidgetItem(str(frame["load_time"]))
            load_item.setTextAlignment(Qt.AlignCenter)
            self.unified_table.setItem(row, 1, load_item)
            
            # Page in Memory (editable)
            page_item = QTableWidgetItem(frame["page"])
            page_item.setTextAlignment(Qt.AlignCenter)
            self.unified_table.setItem(row, 2, page_item)
            
            # Page request columns (empty initially, read-only)
            for col in range(3, total_columns):
                item = QTableWidgetItem("")
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                self.unified_table.setItem(row, col, item)
        
        # Set page sequence input
        self.page_input.setText(",".join(self.page_sequence))
        
        self._updating_table = False
    
    def _rebuild_table_columns(self):
        """Rebuild the table columns when page sequence changes"""
        self._updating_table = True
        
        num_frames = len(self.frames) if self.frames else 5
        num_pages = len(self.page_sequence) if self.page_sequence else 0
        
        total_columns = 3 + num_pages
        self.unified_table.setColumnCount(total_columns)
        
        # Update headers
        headers = ["Frame ID", "Load Time", "Page in Memory"] + self.page_sequence
        self.unified_table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        self.unified_table.setColumnWidth(0, 70)
        self.unified_table.setColumnWidth(1, 75)
        self.unified_table.setColumnWidth(2, 120)
        for i in range(3, total_columns):
            self.unified_table.setColumnWidth(i, 40)
        
        # Add/update page request columns (empty, read-only)
        for row in range(num_frames):
            for col in range(3, total_columns):
                item = self.unified_table.item(row, col)
                if not item:
                    item = QTableWidgetItem("")
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.unified_table.setItem(row, col, item)
                else:
                    item.setText("")
                    item.setBackground(QColor("white"))
                    item.setForeground(QColor("black"))
        
        self._updating_table = False
    
    def _update_clock_display(self, clock_order, r_bits, pointer_index):
        """Update the visual clock blocks with R-bit values and pointer"""
        # Clear existing blocks
        for block in self.clock_blocks:
            block.setParent(None)
        self.clock_blocks.clear()
        
        # Create new blocks with R-bit display and pointer
        for i, frame_id in enumerate(clock_order):
            r_bit = r_bits.get(frame_id, 1)
            is_pointer = (i == pointer_index)
            block = ClockBlockWidget(frame_id, r_bit, is_pointer, self.clock_container)
            if self.current_theme:
                block.set_theme_colors({
                    'queue_block_bg': self.current_theme.get('button_bg', '#4a90e2'),
                    'queue_block_border': self.current_theme.get('button_hover', '#357abd'),
                    'queue_block_text': self.current_theme.get('button_text', 'white'),
                    'rbit_zero_bg': '#ff9800',
                    'rbit_zero_border': '#f57c00',
                    'pointer_color': '#ff5722'
                })
            self.clock_blocks.append(block)
            self.clock_container_layout.addWidget(block)
    
    def _show_step(self, step_index):
        """Display a specific tutorial step"""
        if step_index < 0 or step_index >= len(self.steps):
            return
        
        self.current_step = step_index
        step = self.steps[step_index]
        
        # Update title and description
        self.step_title.setText(step["title"])
        self.step_description.setText(step["description"])
        
        # Update step indicator
        self.step_indicator.setText(f"Step {step_index} of {len(self.steps) - 1}")
        
        # Update navigation buttons
        self.prev_btn.setEnabled(step_index > 0)
        self.next_btn.setEnabled(step_index < len(self.steps) - 1)
        
        # Update unified table
        self._update_unified_table(step["solution_grid"], step["frame_state"])
        
        # Update clock display with pointer
        self._update_clock_display(
            step["clock_order"], 
            step.get("r_bits", {}),
            step.get("pointer_index", -1)
        )
    
    def _update_unified_table(self, solution_grid, frame_state):
        """Update the unified table based on step data"""
        if not self.frames:
            return
        
        self._updating_table = True
        
        # Create frame ID to row mapping
        frame_to_row = {f["id"]: i for i, f in enumerate(self.frames)}
        
        # Reset all page request cells (columns 3+)
        for row in range(self.unified_table.rowCount()):
            for col in range(3, self.unified_table.columnCount()):
                item = self.unified_table.item(row, col)
                if item:
                    item.setText("")
                    item.setBackground(QColor("white"))
                    item.setForeground(QColor("black"))
        
        # Update "Page in Memory" column (col 2) with current frame state
        for frame_id, page in frame_state.items():
            row = frame_to_row.get(frame_id)
            if row is not None:
                item = self.unified_table.item(row, 2)
                if item:
                    item.setText(page)
        
        # Fill in solution grid cells
        for (frame_id, col_idx), cell_data in solution_grid.items():
            row = frame_to_row.get(frame_id)
            if row is not None:
                col = col_idx + 3  # Offset for Frame ID, Load Time, and Page in Memory columns
                item = self.unified_table.item(row, col)
                if item:
                    item.setText(cell_data["text"])
                    if cell_data["is_hit"]:
                        item.setBackground(self.hit_color)
                        item.setForeground(QColor("white"))
                    else:
                        item.setBackground(self.fault_color)
                        item.setForeground(QColor("white"))
        
        self._updating_table = False
    
    def _on_random_clicked(self):
        """Handle random generation button click"""
        self._generate_random_problem()
        self._setup_unified_table()
        self._generate_steps()
        self.current_step = 0
        self._show_step(0)
    
    def _next_step(self):
        """Go to next step"""
        self._show_step(self.current_step + 1)
    
    def _prev_step(self):
        """Go to previous step"""
        self._show_step(self.current_step - 1)
    
    def reset_tutorial(self):
        """Reset tutorial to first step"""
        self._show_step(0)
    
    def showEvent(self, event):
        """Handle show event to refresh when visible"""
        super().showEvent(event)
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            self._update_unified_table(step["solution_grid"], step["frame_state"])
            self._update_clock_display(
                step["clock_order"],
                step.get("r_bits", {}),
                step.get("pointer_index", -1)
            )
    
    def apply_theme(self, theme: dict):
        """Apply theme colors to the tutorial page"""
        self.current_theme = theme
        
        text_color = theme.get('text_primary', '#ffffff')
        text_secondary = theme.get('text_secondary', '#c3c3c3')
        button_bg = theme.get('button_bg', '#7289da')
        button_hover = theme.get('button_hover', '#677bc4')
        input_bg = theme.get('input_bg', '#40444b')
        table_bg = theme.get('table_bg', '#40444b')
        table_grid = theme.get('table_grid', '#72767d')
        header_bg = theme.get('header_bg', '#2c2f33')
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {theme.get('main_bg', '#36393f')};
                color: {text_color};
            }}
            
            QLabel#tutorialTitle {{
                font-size: 28px;
                font-weight: bold;
                color: {button_bg};
                background-color: transparent;
            }}
            
            QLabel#sectionLabel {{
                font-size: 14px;
                font-weight: bold;
                color: {text_color};
                background-color: transparent;
            }}
            
            QPushButton#randomBtn {{
                background-color: {input_bg};
                border: 1px solid {table_grid};
                padding: 10px 20px;
                border-radius: 6px;
                color: {text_color};
                font-size: 14px;
            }}
            
            QPushButton#randomBtn:hover {{
                background-color: {theme.get('sidebar_hover', '#4a4f56')};
                border: 1px solid {button_bg};
            }}
            
            QLabel#stepTitle {{
                font-size: 20px;
                font-weight: bold;
                color: {text_color};
                background-color: transparent;
            }}
            
            QLabel#stepDescription {{
                font-size: 14px;
                color: {text_color};
                background-color: transparent;
                padding: 10px;
            }}
            
            QLabel#stepIndicator {{
                font-size: 14px;
                color: {text_secondary};
                background-color: transparent;
                margin: 0 20px;
            }}
            
            QFrame#stepFrame {{
                background-color: {input_bg};
                border: 1px solid {table_grid};
                border-radius: 8px;
                padding: 15px;
            }}
            
            QScrollArea#descriptionScroll {{
                border: none;
                background-color: transparent;
            }}
            
            QPushButton#backBtn {{
                background-color: {input_bg};
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                color: {text_color};
                font-size: 14px;
            }}
            
            QPushButton#backBtn:hover {{
                background-color: {theme.get('sidebar_hover', '#4a4f56')};
            }}
            
            QPushButton#navBtn {{
                background-color: {button_bg};
                border: none;
                padding: 10px 30px;
                border-radius: 6px;
                color: {theme.get('button_text', '#ffffff')};
                font-size: 14px;
                font-weight: bold;
            }}
            
            QPushButton#navBtn:hover {{
                background-color: {button_hover};
            }}
            
            QPushButton#navBtn:disabled {{
                background-color: {input_bg};
                color: {text_secondary};
            }}
            
            QTableWidget {{
                background-color: {table_bg};
                gridline-color: {table_grid};
                border: 1px solid {table_grid};
                color: {text_color};
            }}
            
            QTableWidget::item {{
                padding: 5px;
            }}
            
            QHeaderView::section {{
                background-color: {header_bg};
                color: {text_color};
                padding: 5px;
                border: 1px solid {table_grid};
            }}
            
            QLineEdit {{
                background-color: {input_bg};
                border: 1px solid {table_grid};
                border-radius: 4px;
                padding: 8px;
                color: {text_color};
            }}
            
            QLineEdit:focus {{
                border: 1px solid {button_bg};
            }}
        """)
        
        # Update clock blocks with theme
        for block in self.clock_blocks:
            block.set_theme_colors({
                'queue_block_bg': button_bg,
                'queue_block_border': button_hover,
                'queue_block_text': theme.get('button_text', 'white'),
                'rbit_zero_bg': '#ff9800',
                'rbit_zero_border': '#f57c00',
                'pointer_color': '#ff5722'
            })
    
    def set_hit_fault_colors(self, hit_color: str, fault_color: str):
        """Set the colors used for hit/fault indicators (for colorblind accessibility)"""
        self.hit_color = QColor(hit_color)
        self.fault_color = QColor(fault_color)
        
        # Refresh the current step display to show new colors
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            self._update_unified_table(step["solution_grid"], step["frame_state"])
