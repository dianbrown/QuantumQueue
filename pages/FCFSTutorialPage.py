"""
FCFS Tutorial Page - Dynamic step-by-step walkthrough of First Come First Served algorithm
Supports custom input or random process generation with per-block step progression
"""

import json
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                              QLabel, QTableWidget, QTableWidgetItem, QFrame,
                              QScrollArea, QHeaderView)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont

# Import the existing ProcessGenerator
from CPU.utils.process_generator import ProcessGenerator


class FCFSTutorialPage(QWidget):
    """Step-by-step FCFS algorithm tutorial page with dynamic step generation"""
    
    # Signal to navigate back to help page
    back_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_step = 0
        self.current_theme = {}
        self.scheduling_block_color = QColor("#ffff00")  # Default yellow
        
        # Process data
        self.processes = []
        self.steps = []
        
        # Flag to prevent recursive updates
        self._updating_table = False
        
        # Load step descriptions from JSON
        self.step_templates = self._load_step_templates()
        
        self.setup_ui()
        
        # Generate initial random set and initialize the tutorial
        self._generate_random_processes()
        self._populate_process_table()
        self._setup_timeline_grid()
        self._generate_steps()
        self._show_step(0)
    
    def _load_step_templates(self):
        """Load step description templates from JSON file"""
        # Try multiple paths for the JSON file
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '..', 'tutorial_kb', 'fcfs_steps.json'),
            os.path.join(os.path.dirname(__file__), '..', '..', 'tutorial_kb', 'fcfs_steps.json'),
            'tutorial_kb/fcfs_steps.json',
        ]
        
        for path in possible_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                continue
        
        # Return default templates if file not found
        return self._get_default_templates()
    
    def _get_default_templates(self):
        """Return default step templates if JSON file not found"""
        return {
            "step_types": {
                "initial": {
                    "title": "Step 0: Initial State",
                    "description": "FCFS (First Come First Served) is a non-preemptive scheduling algorithm.\n\nCore Rules:\n- Processes execute in the order they arrive\n- Once a process starts, it runs to completion\n- Tie-breaker: Process ID (alphabetical order)"
                },
                "show_arrivals": {
                    "title": "Step 1: Sort by Arrival Time",
                    "description": "First, sort all processes by arrival time. If arrivals are equal, use Process ID.\n\nRS (Ready State) markers show when each process enters the ready queue."
                },
                "first_process_first_block": {
                    "title": "Step {step}: Process {process_id} begins execution",
                    "description": "Process {process_id} arrives first at t={arrival} and has burst time of {burst}."
                },
                "process_start": {
                    "title": "Step {step}: Process {process_id} begins execution",
                    "description": "Process {process_id} starts at t={current_time}."
                },
                "continue_block": {
                    "title": "Step {step}: Process {process_id} continues (t={current_time})",
                    "description": "Process {process_id} continues. Block {block_num} of {burst}."
                },
                "process_complete_block": {
                    "title": "Step {step}: Process {process_id} completes",
                    "description": "Process {process_id} completes at t={end_time}."
                },
                "final": {
                    "title": "Step {step}: Final Solution",
                    "description": "FCFS Scheduling Complete!"
                }
            }
        }
    
    def _generate_random_processes(self):
        """Generate random process values using the main app's ProcessGenerator"""
        # Use the existing ProcessGenerator with unique arrivals for FCFS
        generated = ProcessGenerator.generate_processes(num_processes=4, unique_arrivals=True)
        
        self.processes = []
        for proc in generated:
            self.processes.append({
                "id": proc.id,
                "priority": proc.priority,
                "arrival": proc.arrival,
                "burst": proc.burst
            })
    
    def _get_processes_from_table(self):
        """Read process values from the process table"""
        self.processes = []
        for row in range(self.process_table.rowCount()):
            try:
                process_id = self.process_table.item(row, 0).text() if self.process_table.item(row, 0) else chr(ord('A') + row)
                priority = int(self.process_table.item(row, 1).text()) if self.process_table.item(row, 1) else 1
                arrival = int(self.process_table.item(row, 2).text()) if self.process_table.item(row, 2) else 1
                burst = int(self.process_table.item(row, 3).text()) if self.process_table.item(row, 3) else 1
                
                # Validate values
                priority = max(1, min(10, priority))
                arrival = max(1, min(30, arrival))
                burst = max(1, min(15, burst))
                
                self.processes.append({
                    "id": process_id,
                    "priority": priority,
                    "arrival": arrival,
                    "burst": burst
                })
            except (ValueError, AttributeError):
                # Use defaults if parsing fails
                self.processes.append({
                    "id": chr(ord('A') + row),
                    "priority": 1,
                    "arrival": 1,
                    "burst": 3
                })
    
    def _on_table_cell_changed(self, row, column):
        """Handle cell value changes in the process table"""
        # Skip if we're currently updating the table programmatically
        if self._updating_table:
            return
        
        # Skip the Process ID column (column 0)
        if column == 0:
            return
        
        # Read all values from table and regenerate steps
        self._get_processes_from_table()
        self._generate_steps()
        self.current_step = 0
        self._setup_timeline_grid()
        self._show_step(0)
    
    def _generate_steps(self):
        """Generate tutorial steps dynamically based on current processes"""
        self.steps = []
        templates = self.step_templates.get("step_types", {})
        
        # Sort processes by arrival, then by ID (FCFS order)
        sorted_procs = sorted(self.processes, key=lambda p: (p['arrival'], p['id']))
        process_list = ", ".join([p['id'] for p in self.processes])
        sorted_order = " -> ".join([f"{p['id']}({p['arrival']})" for p in sorted_procs])
        
        # Build RS markers dict
        rs_markers = {p['id']: [p['arrival']] for p in self.processes}
        
        # Step 0: Initial State
        initial = templates.get("initial", {})
        self.steps.append({
            "title": initial.get("title", "Step 0: Initial State"),
            "description": initial.get("description", "").format(
                num_processes=len(self.processes),
                process_list=process_list
            ),
            "timeline": {},
            "rs_markers": {}
        })
        
        # Step 1: Show RS markers
        arrivals = templates.get("show_arrivals", {})
        self.steps.append({
            "title": arrivals.get("title", "Step 1: Sort by Arrival Time"),
            "description": arrivals.get("description", "").format(
                sorted_order=sorted_order
            ),
            "timeline": {},
            "rs_markers": rs_markers.copy()
        })
        
        # Generate per-block steps
        step_num = 2
        current_time = 1
        timeline = {}
        start_times = {}
        end_times = {}
        prev_process = None
        prev_end = None
        
        for proc_idx, proc in enumerate(sorted_procs):
            pid = proc['id']
            burst = proc['burst']
            arrival = proc['arrival']
            
            # Advance to arrival if needed
            if current_time < arrival:
                current_time = arrival
            
            start_times[pid] = current_time
            
            # Generate a step for each block of this process
            for block_num in range(1, burst + 1):
                # Initialize timeline for this process if needed
                if pid not in timeline:
                    timeline[pid] = []
                
                # Add current time block
                timeline[pid].append(current_time)
                
                # Determine step type and description
                is_first_process = (proc_idx == 0)
                is_first_block = (block_num == 1)
                is_last_block = (block_num == burst)
                remaining = burst - block_num
                
                if is_first_block:
                    if is_first_process:
                        # First process, first block
                        tmpl = templates.get("first_process_first_block", {})
                        title = tmpl.get("title", "Step {step}: Process {process_id} begins")
                        desc = tmpl.get("description", "Process {process_id} starts.")
                    else:
                        # Subsequent process starts
                        tmpl = templates.get("process_start", {})
                        title = tmpl.get("title", "Step {step}: Process {process_id} begins")
                        desc = tmpl.get("description", "Process {process_id} starts.")
                        
                        # Context about waiting
                        wait_context = f" (while {prev_process} was running)" if prev_process else ""
                        wait_time = current_time - arrival
                        wait_info = f"{pid} waited from t={arrival} to t={current_time} (waiting time = {wait_time})." if wait_time > 0 else f"{pid} starts immediately upon arriving."
                        
                        desc = desc.format(
                            step=step_num,
                            process_id=pid,
                            arrival=arrival,
                            burst=burst,
                            current_time=current_time,
                            prev_process=prev_process or "N/A",
                            prev_end=prev_end or "N/A",
                            wait_context=wait_context,
                            wait_info=wait_info
                        )
                        title = title.format(step=step_num, process_id=pid, current_time=current_time)
                        
                        self.steps.append({
                            "title": title,
                            "description": desc,
                            "timeline": {k: v.copy() for k, v in timeline.items()},
                            "rs_markers": rs_markers.copy()
                        })
                        step_num += 1
                        current_time += 1
                        continue
                    
                    title = title.format(step=step_num, process_id=pid, current_time=current_time)
                    desc = desc.format(
                        step=step_num,
                        process_id=pid,
                        arrival=arrival,
                        burst=burst,
                        current_time=current_time
                    )
                elif is_last_block:
                    # Last block - process completes
                    end_time = current_time + 1
                    end_times[pid] = end_time
                    wait_time = start_times[pid] - arrival
                    
                    tmpl = templates.get("process_complete_block", {})
                    title = tmpl.get("title", "Step {step}: Process {process_id} completes")
                    desc = tmpl.get("description", "Process {process_id} completes.")
                    
                    title = title.format(step=step_num, process_id=pid, current_time=current_time)
                    desc = desc.format(
                        step=step_num,
                        process_id=pid,
                        start_time=start_times[pid],
                        end_time=end_time,
                        burst=burst,
                        wait_time=wait_time,
                        arrival=arrival,
                        current_time=current_time
                    )
                    
                    prev_process = pid
                    prev_end = end_time
                else:
                    # Middle block - continue
                    tmpl = templates.get("continue_block", {})
                    title = tmpl.get("title", "Step {step}: Process {process_id} continues")
                    desc = tmpl.get("description", "Process {process_id} continues.")
                    
                    title = title.format(step=step_num, process_id=pid, current_time=current_time)
                    desc = desc.format(
                        step=step_num,
                        process_id=pid,
                        block_num=block_num,
                        burst=burst,
                        remaining=remaining,
                        current_time=current_time
                    )
                
                self.steps.append({
                    "title": title,
                    "description": desc,
                    "timeline": {k: v.copy() for k, v in timeline.items()},
                    "rs_markers": rs_markers.copy()
                })
                step_num += 1
                current_time += 1
            
            # Record end time
            end_times[pid] = current_time
        
        # Final step with metrics
        execution_order = " -> ".join([p['id'] for p in sorted_procs])
        metrics_lines = []
        total_wait = 0
        total_tat = 0
        
        for proc in sorted_procs:
            pid = proc['id']
            start = start_times.get(pid, 0)
            end = end_times.get(pid, 0)
            burst = proc['burst']
            arrival = proc['arrival']
            tat = end - arrival
            wait = start - arrival
            total_wait += wait
            total_tat += tat
            metrics_lines.append(f"- Process {pid}: Start={start}, End={end}, TAT={tat}, WT={wait}")
        
        metrics = "\n".join(metrics_lines)
        avg_wait = total_wait / len(self.processes) if self.processes else 0
        avg_tat = total_tat / len(self.processes) if self.processes else 0
        
        final_tmpl = templates.get("final", {})
        self.steps.append({
            "title": final_tmpl.get("title", "Final Solution").format(step=step_num),
            "description": final_tmpl.get("description", "Complete!").format(
                step=step_num,
                execution_order=execution_order,
                metrics=metrics,
                avg_wait=f"{avg_wait:.2f}",
                avg_tat=f"{avg_tat:.2f}"
            ),
            "timeline": {k: v.copy() for k, v in timeline.items()},
            "rs_markers": rs_markers.copy()
        })
        
        # Update step indicator
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
        
        # Random generation button (no emoji)
        self.random_btn = QPushButton("Generate Random")
        self.random_btn.setObjectName("randomBtn")
        self.random_btn.setCursor(Qt.PointingHandCursor)
        self.random_btn.clicked.connect(self._on_random_clicked)
        top_layout.addWidget(self.random_btn)
        
        layout.addLayout(top_layout)
        
        # Title
        self.page_title = QLabel("FCFS Tutorial")
        self.page_title.setObjectName("tutorialTitle")
        layout.addWidget(self.page_title)
        
        # Process table (original style, but editable)
        self.process_table = QTableWidget(4, 4)
        self.process_table.setHorizontalHeaderLabels(["Process ID", "Priority", "Arrival", "Burst time"])
        self.process_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.process_table.setMaximumHeight(170)
        self.process_table.cellChanged.connect(self._on_table_cell_changed)
        layout.addWidget(self.process_table)
        
        # Timeline grid
        self.timeline_grid = QTableWidget(4, 33)
        headers = ["Process ID"] + [str(i) for i in range(1, 33)]
        self.timeline_grid.setHorizontalHeaderLabels(headers)
        self.timeline_grid.setColumnWidth(0, 80)
        for i in range(1, 33):
            self.timeline_grid.setColumnWidth(i, 35)
        self.timeline_grid.verticalHeader().setDefaultSectionSize(30)
        self.timeline_grid.verticalHeader().hide()
        self._setup_timeline_grid()
        layout.addWidget(self.timeline_grid)
        
        # Step info section
        step_frame = QFrame()
        step_frame.setObjectName("stepFrame")
        step_layout = QVBoxLayout(step_frame)
        
        self.step_title = QLabel("Step 0: Initial State")
        self.step_title.setObjectName("stepTitle")
        step_layout.addWidget(self.step_title)
        
        # Scroll area for description
        desc_scroll = QScrollArea()
        desc_scroll.setWidgetResizable(True)
        desc_scroll.setMaximumHeight(200)
        desc_scroll.setObjectName("descriptionScroll")
        
        self.step_description = QLabel("")
        self.step_description.setObjectName("stepDescription")
        self.step_description.setWordWrap(True)
        self.step_description.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        desc_scroll.setWidget(self.step_description)
        step_layout.addWidget(desc_scroll)
        
        layout.addWidget(step_frame)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        nav_layout.addStretch()
        
        self.prev_btn = QPushButton("Previous")
        self.prev_btn.setObjectName("navBtn")
        self.prev_btn.setCursor(Qt.PointingHandCursor)
        self.prev_btn.clicked.connect(self._prev_step)
        nav_layout.addWidget(self.prev_btn)
        
        self.step_indicator = QLabel("Step 0 of 6")
        self.step_indicator.setObjectName("stepIndicator")
        nav_layout.addWidget(self.step_indicator)
        
        self.next_btn = QPushButton("Next")
        self.next_btn.setObjectName("navBtn")
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.clicked.connect(self._next_step)
        nav_layout.addWidget(self.next_btn)
        
        nav_layout.addStretch()
        layout.addLayout(nav_layout)
    
    def _populate_process_table(self):
        """Fill the process table with current process data"""
        self._updating_table = True
        for i, proc in enumerate(self.processes):
            # Process ID (read-only)
            id_item = QTableWidgetItem(proc["id"])
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            id_item.setTextAlignment(Qt.AlignCenter)
            self.process_table.setItem(i, 0, id_item)
            
            # Priority (editable)
            priority_item = QTableWidgetItem(str(proc["priority"]))
            priority_item.setTextAlignment(Qt.AlignCenter)
            self.process_table.setItem(i, 1, priority_item)
            
            # Arrival (editable)
            arrival_item = QTableWidgetItem(str(proc["arrival"]))
            arrival_item.setTextAlignment(Qt.AlignCenter)
            self.process_table.setItem(i, 2, arrival_item)
            
            # Burst (editable)
            burst_item = QTableWidgetItem(str(proc["burst"]))
            burst_item.setTextAlignment(Qt.AlignCenter)
            self.process_table.setItem(i, 3, burst_item)
        self._updating_table = False
    
    def _on_random_clicked(self):
        """Handle random generation button click"""
        self._generate_random_processes()
        self._populate_process_table()
        self._generate_steps()
        self.current_step = 0
        self._setup_timeline_grid()
        self._show_step(0)
    
    def _setup_timeline_grid(self):
        """Initialize the timeline grid with process IDs"""
        for i, proc in enumerate(self.processes[:4]):
            # Process ID column
            item = QTableWidgetItem(proc["id"])
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item.setTextAlignment(Qt.AlignCenter)
            self.timeline_grid.setItem(i, 0, item)
            
            # Timeline columns
            for j in range(1, 33):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(Qt.white)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.timeline_grid.setItem(i, j, item)
    
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
        
        # Clear and update timeline grid
        self._update_timeline(step["timeline"], step["rs_markers"])
    
    def _update_timeline(self, timeline_data, rs_markers):
        """Update the timeline grid based on step data"""
        # Skip if timeline grid is not fully initialized
        if not self.timeline_grid:
            return
            
        # Create process ID to row mapping
        process_to_row = {proc["id"]: i for i, proc in enumerate(self.processes[:4])}
        
        # Clear all cells first
        for row in range(4):
            for col in range(1, 33):
                item = self.timeline_grid.item(row, col)
                if item:
                    item.setBackground(Qt.white)
                    item.setText("")
                    item.setForeground(QColor(0, 0, 0))
        
        # Fill scheduled blocks
        for process_id, times in timeline_data.items():
            row = process_to_row.get(process_id)
            if row is not None:
                for t in times:
                    if 1 <= t <= 32:
                        item = self.timeline_grid.item(row, t)
                        if item:
                            item.setBackground(self.scheduling_block_color)
                            item.setText("-")
                            item.setForeground(QColor(0, 0, 0))
        
        # Add RS markers
        for process_id, times in rs_markers.items():
            row = process_to_row.get(process_id)
            if row is not None:
                for t in times:
                    if 1 <= t <= 32:
                        item = self.timeline_grid.item(row, t)
                        if item:
                            current_text = item.text()
                            if current_text and current_text != "":
                                item.setText(f"{current_text}\nRS")
                            else:
                                item.setText("RS")
                            item.setForeground(QColor(128, 128, 128))  # Gray for RS
    
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
        """Handle show event to refresh timeline when visible"""
        super().showEvent(event)
        # Refresh the current step when the page becomes visible
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            self._update_timeline(step["timeline"], step["rs_markers"])
    
    def apply_theme(self, theme: dict):
        """Apply theme colors to the tutorial page"""
        self.current_theme = theme
        
        # Update scheduling block color from theme
        if 'scheduling_block_bg' in theme:
            self.scheduling_block_color = QColor(theme['scheduling_block_bg'])
        
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
        """)
        
        # Refresh the timeline with current step to apply new colors
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            self._update_timeline(step["timeline"], step["rs_markers"])
