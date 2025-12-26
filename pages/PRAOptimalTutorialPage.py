"""
PRA Optimal Tutorial Page - Step-by-step walkthrough of Optimal (Farthest in Future) Algorithm
No queue - uses future page access distances to select victim
Uses a unified table for frame input and solution display
"""

import json
import os
import random
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                              QLabel, QTableWidget, QTableWidgetItem, QFrame,
                              QScrollArea, QHeaderView, QLineEdit)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

# Resource helper (PyInstaller-safe)
from resource_path import load_json_resource


class PRAOptimalTutorialPage(QWidget):
    """Step-by-step Optimal Page Replacement Algorithm tutorial"""
    
    back_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_step = 0
        self.current_theme = {}
        self.hit_color = QColor("#4caf50")
        self.fault_color = QColor("#f44336")
        
        self.frames = []
        self.page_sequence = []
        self.steps = []
        
        self._updating_table = False
        self.step_templates = self._load_step_templates()
        
        self.setup_ui()
        self._generate_random_problem()
        self._setup_unified_table()
        self._generate_steps()
        self._show_step(0)
    
    def _load_step_templates(self):
        """Load step description templates from JSON file"""
        templates = load_json_resource('tutorial_kb/pra_optimal_steps.json', default=None)
        if isinstance(templates, dict) and templates.get('step_types'):
            return templates
        return {"step_types": {}}
    
    def _generate_random_problem(self):
        """Generate random frame data and page sequence"""
        num_frames = 5
        
        self.frames = []
        
        available_load_times = list(range(1, 21))
        random.shuffle(available_load_times)
        selected_load_times = available_load_times[:num_frames]
        
        used_pages = set()
        for i in range(num_frames):
            frame_id = str(num_frames - 1 - i)
            load_time = selected_load_times[i]
            
            page = random.randint(1, 15)
            while page in used_pages:
                page = random.randint(1, 15)
            used_pages.add(page)
            
            self.frames.append({
                "id": frame_id,
                "load_time": load_time,
                "page": str(page)
            })
        
        sequence_length = random.randint(8, 16)
        self.page_sequence = []
        
        for _ in range(sequence_length):
            page = random.randint(1, 15)
            self.page_sequence.append(str(page))
    
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
    
    def _find_future_distance(self, page, current_idx):
        """Find distance to next use of page in sequence (starting after current_idx)"""
        for i in range(current_idx + 1, len(self.page_sequence)):
            if self.page_sequence[i] == page:
                return i - current_idx
        return float('inf')  # Never used again
    
    def _generate_steps(self):
        """Generate tutorial steps dynamically based on current data"""
        self.steps = []
        templates = self.step_templates.get("step_types", {})
        
        if not self.frames or not self.page_sequence:
            return
        
        # Build initial frame state
        frame_state = {f["id"]: f["page"] for f in self.frames}
        frame_list = ", ".join([f"F{f['id']}={f['page']}" for f in self.frames])
        
        # Step 0: Initial State
        initial = templates.get("initial", {})
        self.steps.append({
            "title": initial.get("title", "Step 0: Initial State"),
            "description": initial.get("description", "").format(
                num_frames=len(self.frames),
                frame_list=frame_list
            ),
            "solution_grid": {},
            "frame_state": frame_state.copy()
        })
        
        # Process each page request
        step_num = 1
        solution_grid = {}
        page_hits = 0
        page_faults = 0
        
        for col_idx, requested_page in enumerate(self.page_sequence):
            # Check if page is in memory (HIT)
            hit_frame = None
            for frame_id, page in frame_state.items():
                if page == requested_page:
                    hit_frame = frame_id
                    break
            
            if hit_frame:
                # PAGE HIT
                page_hits += 1
                
                solution_grid[(hit_frame, col_idx)] = {"text": requested_page, "is_hit": True}
                
                hit_tmpl = templates.get("page_hit", {})
                self.steps.append({
                    "title": hit_tmpl.get("title", f"Step {step_num}: HIT").format(
                        step=step_num, page=requested_page
                    ),
                    "description": hit_tmpl.get("description", "").format(
                        step=step_num, page=requested_page, frame_id=hit_frame
                    ),
                    "solution_grid": {k: v.copy() for k, v in solution_grid.items()},
                    "frame_state": frame_state.copy()
                })
            else:
                # PAGE FAULT - need to find optimal victim
                page_faults += 1
                
                # Calculate future distance for each page in memory
                distances = {}
                for frame_id, page in frame_state.items():
                    dist = self._find_future_distance(page, col_idx)
                    distances[frame_id] = (page, dist)
                
                # Build distance analysis text
                distance_lines = []
                for frame_id in sorted(distances.keys()):
                    page, dist = distances[frame_id]
                    if dist == float('inf'):
                        distance_lines.append(f"- Frame {frame_id} (Page {page}): NEVER used again (infinity)")
                    else:
                        next_use_idx = col_idx + dist + 1
                        distance_lines.append(f"- Frame {frame_id} (Page {page}): Next use at position {next_use_idx} (distance = {dist})")
                distance_analysis = "\n".join(distance_lines)
                
                # Find victim: max distance, tie-break by lowest frame ID
                max_dist = -1
                victim_frame = None
                for frame_id in sorted(distances.keys()):
                    page, dist = distances[frame_id]
                    if dist == float('inf'):
                        # Never used again - highest priority
                        if max_dist != float('inf'):
                            max_dist = float('inf')
                            victim_frame = frame_id
                        elif victim_frame is None or frame_id < victim_frame:
                            victim_frame = frame_id
                    elif dist > max_dist and max_dist != float('inf'):
                        max_dist = dist
                        victim_frame = frame_id
                
                old_page = frame_state[victim_frame]
                victim_dist = distances[victim_frame][1]
                
                # Build victim reason
                if victim_dist == float('inf'):
                    # Check if multiple never used again
                    never_used = [fid for fid, (p, d) in distances.items() if d == float('inf')]
                    if len(never_used) > 1:
                        victim_reason = f"Multiple pages never used again ({', '.join([f'F{fid}' for fid in sorted(never_used)])}). Tie-breaker: lowest frame ID = F{victim_frame}"
                    else:
                        victim_reason = f"Page {old_page} is NEVER used again - highest priority for replacement"
                else:
                    # Check if multiple with same distance
                    same_dist = [fid for fid, (p, d) in distances.items() if d == victim_dist]
                    if len(same_dist) > 1:
                        victim_reason = f"Multiple pages with same distance ({', '.join([f'F{fid}' for fid in sorted(same_dist)])}). Tie-breaker: lowest frame ID = F{victim_frame}"
                    else:
                        victim_reason = f"Page {old_page} has the farthest next use (distance = {victim_dist})"
                
                # Update frame state
                frame_state[victim_frame] = requested_page
                
                # Mark this cell in solution grid
                solution_grid[(victim_frame, col_idx)] = {"text": requested_page, "is_hit": False}
                
                fault_tmpl = templates.get("page_fault", {})
                self.steps.append({
                    "title": fault_tmpl.get("title", f"Step {step_num}: FAULT").format(
                        step=step_num, page=requested_page
                    ),
                    "description": fault_tmpl.get("description", "").format(
                        step=step_num, page=requested_page, victim_frame=victim_frame,
                        old_page=old_page, distance_analysis=distance_analysis,
                        victim_reason=victim_reason
                    ),
                    "solution_grid": {k: v.copy() for k, v in solution_grid.items()},
                    "frame_state": frame_state.copy()
                })
            
            step_num += 1
        
        # Final step with statistics
        total_requests = len(self.page_sequence)
        hit_ratio = f"{(page_hits / total_requests * 100):.1f}%" if total_requests > 0 else "0%"
        fault_ratio = f"{(page_faults / total_requests * 100):.1f}%" if total_requests > 0 else "0%"
        
        frame_contents = "\n".join([f"- Frame {fid}: Page {page}" for fid, page in frame_state.items()])
        
        final_tmpl = templates.get("final", {})
        self.steps.append({
            "title": final_tmpl.get("title", "Final Results").format(step=step_num),
            "description": final_tmpl.get("description", "").format(
                step=step_num,
                frame_contents=frame_contents,
                total_requests=total_requests,
                page_hits=page_hits,
                page_faults=page_faults,
                hit_ratio=hit_ratio,
                fault_ratio=fault_ratio
            ),
            "solution_grid": {k: v.copy() for k, v in solution_grid.items()},
            "frame_state": frame_state.copy()
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
        self.page_title = QLabel("Optimal Page Replacement Tutorial")
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
        
        # No queue visualization for Optimal - it uses future distances instead
        
        # Step info section
        step_frame = QFrame()
        step_frame.setObjectName("stepFrame")
        step_layout = QVBoxLayout(step_frame)
        step_layout.setSpacing(5)
        step_layout.setContentsMargins(15, 15, 15, 15)
        
        self.step_title = QLabel("Step 0: Initial State")
        self.step_title.setObjectName("stepTitle")
        step_layout.addWidget(self.step_title)
        
        desc_scroll = QScrollArea()
        desc_scroll.setWidgetResizable(True)
        desc_scroll.setMinimumHeight(150)
        desc_scroll.setMaximumHeight(220)  # Slightly taller for detailed descriptions
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
    
    def _show_step(self, step_index):
        """Display a specific tutorial step"""
        if step_index < 0 or step_index >= len(self.steps):
            return
        
        self.current_step = step_index
        step = self.steps[step_index]
        
        self.step_title.setText(step["title"])
        self.step_description.setText(step["description"])
        self.step_indicator.setText(f"Step {step_index} of {len(self.steps) - 1}")
        
        self.prev_btn.setEnabled(step_index > 0)
        self.next_btn.setEnabled(step_index < len(self.steps) - 1)
        
        self._update_unified_table(step["solution_grid"], step["frame_state"])
    
    def _update_unified_table(self, solution_grid, frame_state):
        """Update the unified table based on step data"""
        if not self.frames:
            return
        
        self._updating_table = True
        
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
        self._show_step(self.current_step + 1)
    
    def _prev_step(self):
        self._show_step(self.current_step - 1)
    
    def reset_tutorial(self):
        self._show_step(0)
    
    def showEvent(self, event):
        super().showEvent(event)
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            self._update_unified_table(step["solution_grid"], step["frame_state"])
    
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
        
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            self._update_unified_table(step["solution_grid"], step["frame_state"])
    
    def set_hit_fault_colors(self, hit_color: str, fault_color: str):
        """Set the colors used for hit/fault indicators (for colorblind accessibility)"""
        self.hit_color = QColor(hit_color)
        self.fault_color = QColor(fault_color)
        
        # Refresh the current step display to show new colors
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            self._update_unified_table(step["solution_grid"], step["frame_state"])
