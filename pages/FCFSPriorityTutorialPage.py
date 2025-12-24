"""
FCFS Priority Tutorial Page - Step-by-step walkthrough of FCFS with Priority (Preemptive) algorithm
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


class FCFSPriorityTutorialPage(QWidget):
    """Step-by-step FCFS Priority algorithm tutorial page with dynamic step generation"""
    
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
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '..', 'tutorial_kb', 'fcfs_priority_steps.json'),
            os.path.join(os.path.dirname(__file__), '..', '..', 'tutorial_kb', 'fcfs_priority_steps.json'),
            'tutorial_kb/fcfs_priority_steps.json',
        ]
        
        for path in possible_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                continue
        
        return self._get_default_templates()
    
    def _get_default_templates(self):
        """Return default step templates if JSON file not found"""
        return {
            "step_types": {
                "initial": {
                    "title": "Step 0: Initial State",
                    "description": "FCFS with Priority is a PREEMPTIVE scheduling algorithm."
                },
                "show_arrivals": {
                    "title": "Step 1: Mark Arrival Times (RS)",
                    "description": "RS markers show when each process arrives."
                },
                "first_block": {
                    "title": "Step {step}: Process {process_id} begins",
                    "description": "Process {process_id} starts execution."
                },
                "continue_block": {
                    "title": "Step {step}: Process {process_id} continues",
                    "description": "Process {process_id} continues."
                },
                "preemption": {
                    "title": "Step {step}: PREEMPTION!",
                    "description": "Higher priority process preempts current."
                },
                "process_complete": {
                    "title": "Step {step}: Process {process_id} completes",
                    "description": "Process completes."
                },
                "final": {
                    "title": "Step {step}: Final Solution",
                    "description": "Complete!"
                }
            }
        }
    
    def _generate_random_processes(self):
        """Generate random process values using the main app's ProcessGenerator"""
        generated = ProcessGenerator.generate_processes(num_processes=4, unique_arrivals=False)
        
        self.processes = []
        for proc in generated:
            self.processes.append({
                "id": proc.id,
                "priority": proc.priority,
                "arrival": proc.arrival,
                "burst": proc.burst
            })
    
    def _get_processes_from_table(self):
        """Read process values from the unified table (columns 0-3 of timeline_grid)"""
        self.processes = []
        for row in range(4):
            try:
                process_id = self.timeline_grid.item(row, 0).text() if self.timeline_grid.item(row, 0) else chr(ord('A') + row)
                priority = int(self.timeline_grid.item(row, 1).text()) if self.timeline_grid.item(row, 1) else 1
                arrival = int(self.timeline_grid.item(row, 2).text()) if self.timeline_grid.item(row, 2) else 1
                burst = int(self.timeline_grid.item(row, 3).text()) if self.timeline_grid.item(row, 3) else 1
                
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
                self.processes.append({
                    "id": chr(ord('A') + row),
                    "priority": 1,
                    "arrival": 1,
                    "burst": 3
                })
    
    def _on_table_cell_changed(self, row, column):
        """Handle cell value changes in the process table"""
        if self._updating_table:
            return
        # Only react to editable columns 1-3 (Priority, Arrival, Burst)
        if column < 1 or column > 3:
            return
        
        self._get_processes_from_table()
        self._generate_steps()
        self.current_step = 0
        self._setup_timeline_grid()
        self._show_step(0)
    
    def _generate_steps(self):
        """Generate tutorial steps dynamically for FCFS Priority (Preemptive)"""
        self.steps = []
        templates = self.step_templates.get("step_types", {})
        
        # Process state tracking
        process_map = {p['id']: p.copy() for p in self.processes}
        for pid in process_map:
            process_map[pid]['remaining'] = process_map[pid]['burst']
            process_map[pid]['rs_time'] = process_map[pid]['arrival']
            process_map[pid]['started'] = False
            process_map[pid]['start_time'] = None
            process_map[pid]['completed'] = False
        
        process_list = ", ".join([f"{p['id']}(P{p['priority']})" for p in self.processes])
        arrival_order = " → ".join([f"{p['id']} at t={p['arrival']}" for p in sorted(self.processes, key=lambda x: (x['arrival'], x['id']))])
        
        # RS markers - initially just arrivals
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
            "title": arrivals.get("title", "Step 1: Mark Arrival Times"),
            "description": arrivals.get("description", "").format(
                arrival_order=arrival_order
            ),
            "timeline": {},
            "rs_markers": {k: v.copy() for k, v in rs_markers.items()}
        })
        
        # Simulate FCFS Priority algorithm step by step
        step_num = 2
        current_time = 1
        timeline = {}
        current_process = None
        ready_queue = []
        start_times = {}
        end_times = {}
        execution_order = []
        
        max_time = 32
        
        while current_time <= max_time:
            # Check for newly arrived processes
            new_arrivals = []
            for pid, proc in process_map.items():
                if proc['arrival'] == current_time and not proc['completed'] and proc['remaining'] > 0:
                    if pid not in [p['id'] for p in ready_queue] and (current_process is None or current_process['id'] != pid):
                        new_arrivals.append(proc)
                        ready_queue.append(proc)
            
            # Check for preemption
            if new_arrivals and current_process:
                for new_proc in new_arrivals:
                    if new_proc['priority'] > current_process['priority']:
                        # Preemption occurs!
                        tmpl = templates.get("preemption", {})
                        title = tmpl.get("title", "PREEMPTION!").format(
                            step=step_num,
                            new_process=new_proc['id'],
                            old_process=current_process['id']
                        )
                        
                        # Update RS time for preempted process
                        current_process['rs_time'] = current_time
                        if current_process['id'] not in rs_markers:
                            rs_markers[current_process['id']] = []
                        rs_markers[current_process['id']].append(current_time)
                        
                        desc = tmpl.get("description", "").format(
                            new_process=new_proc['id'],
                            new_priority=new_proc['priority'],
                            old_process=current_process['id'],
                            old_priority=current_process['priority'],
                            current_time=current_time,
                            new_rs=current_time,
                            old_remaining=current_process['remaining']
                        )
                        
                        self.steps.append({
                            "title": title,
                            "description": desc,
                            "timeline": {k: v.copy() for k, v in timeline.items()},
                            "rs_markers": {k: v.copy() for k, v in rs_markers.items()}
                        })
                        step_num += 1
                        
                        # Add preempted process back to ready queue if not already there
                        if current_process not in ready_queue:
                            ready_queue.append(current_process)
                        current_process = None
                        break
            
            # Select process from ready queue if no current process
            if current_process is None and ready_queue:
                # Sort by: priority (desc), rs_time (asc), id (asc)
                ready_queue.sort(key=lambda p: (-p['priority'], p['rs_time'], p['id']))
                current_process = ready_queue.pop(0)
                
                if not current_process['started']:
                    current_process['started'] = True
                    current_process['start_time'] = current_time
                    start_times[current_process['id']] = current_time
                    if current_process['id'] not in execution_order:
                        execution_order.append(current_process['id'])
                    
                    # First block for this process
                    tmpl = templates.get("first_block", {})
                    title = tmpl.get("title", "Process starts").format(
                        step=step_num,
                        process_id=current_process['id'],
                        priority=current_process['priority']
                    )
                    desc = tmpl.get("description", "").format(
                        step=step_num,
                        process_id=current_process['id'],
                        priority=current_process['priority'],
                        arrival=current_process['arrival'],
                        burst=current_process['burst'],
                        current_time=current_time
                    )
                else:
                    # Resuming after preemption
                    tmpl = templates.get("resume_after_preemption", templates.get("continue_block", {}))
                    title = tmpl.get("title", "Process resumes").format(
                        step=step_num,
                        process_id=current_process['id'],
                        priority=current_process['priority'],
                        current_time=current_time
                    )
                    desc = tmpl.get("description", "").format(
                        step=step_num,
                        process_id=current_process['id'],
                        priority=current_process['priority'],
                        preemption_time=current_process['rs_time'],
                        current_time=current_time,
                        rs_time=current_process['rs_time'],
                        remaining=current_process['remaining']
                    )
            elif current_process:
                # Continue current process
                block_num = current_process['burst'] - current_process['remaining'] + 1
                remaining = current_process['remaining'] - 1
                
                if remaining == 0:
                    # Process completes
                    tmpl = templates.get("process_complete", {})
                    title = tmpl.get("title", "Process completes").format(
                        step=step_num,
                        process_id=current_process['id']
                    )
                    
                    end_time = current_time + 1
                    end_times[current_process['id']] = end_time
                    tat = end_time - current_process['arrival']
                    wait_time = tat - current_process['burst']
                    
                    desc = tmpl.get("description", "").format(
                        step=step_num,
                        process_id=current_process['id'],
                        priority=current_process['priority'],
                        start_time=start_times.get(current_process['id'], current_time),
                        end_time=end_time,
                        burst=current_process['burst'],
                        wait_time=wait_time,
                        tat=tat
                    )
                else:
                    tmpl = templates.get("continue_block", {})
                    title = tmpl.get("title", "Process continues").format(
                        step=step_num,
                        process_id=current_process['id'],
                        current_time=current_time
                    )
                    desc = tmpl.get("description", "").format(
                        step=step_num,
                        process_id=current_process['id'],
                        priority=current_process['priority'],
                        block_num=block_num,
                        burst=current_process['burst'],
                        remaining=remaining,
                        current_time=current_time
                    )
            else:
                # No process to run, advance time
                current_time += 1
                continue
            
            # Execute one time unit
            if current_process:
                if current_process['id'] not in timeline:
                    timeline[current_process['id']] = []
                timeline[current_process['id']].append(current_time)
                
                self.steps.append({
                    "title": title,
                    "description": desc,
                    "timeline": {k: v.copy() for k, v in timeline.items()},
                    "rs_markers": {k: v.copy() for k, v in rs_markers.items()}
                })
                step_num += 1
                
                current_process['remaining'] -= 1
                process_map[current_process['id']]['remaining'] = current_process['remaining']
                
                if current_process['remaining'] == 0:
                    current_process['completed'] = True
                    process_map[current_process['id']]['completed'] = True
                    current_process = None
            
            current_time += 1
            
            # Check if all processes are complete
            all_complete = all(p['completed'] for p in process_map.values())
            if all_complete:
                break
        
        # Final step with metrics
        exec_order_str = " → ".join(execution_order)
        metrics_lines = []
        total_wait = 0
        total_tat = 0
        
        for proc in self.processes:
            pid = proc['id']
            start = start_times.get(pid, 0)
            end = end_times.get(pid, 0)
            burst = proc['burst']
            arrival = proc['arrival']
            tat = end - arrival if end > 0 else 0
            wait = tat - burst if tat > 0 else 0
            total_wait += wait
            total_tat += tat
            metrics_lines.append(f"- Process {pid}: Priority={proc['priority']}, TAT={tat}, WT={wait}")
        
        metrics = "\n".join(metrics_lines)
        avg_wait = total_wait / len(self.processes) if self.processes else 0
        avg_tat = total_tat / len(self.processes) if self.processes else 0
        
        final_tmpl = templates.get("final", {})
        self.steps.append({
            "title": final_tmpl.get("title", "Final Solution").format(step=step_num),
            "description": final_tmpl.get("description", "Complete!").format(
                step=step_num,
                execution_order=exec_order_str,
                metrics=metrics,
                avg_wait=f"{avg_wait:.2f}",
                avg_tat=f"{avg_tat:.2f}"
            ),
            "timeline": {k: v.copy() for k, v in timeline.items()},
            "rs_markers": {k: v.copy() for k, v in rs_markers.items()}
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
        self.page_title = QLabel("FCFS Priority Tutorial")
        self.page_title.setObjectName("tutorialTitle")
        layout.addWidget(self.page_title)
        
        # Unified table: Process info + Timeline (1-32)
        self.timeline_grid = QTableWidget(4, 36)
        headers = ["Process ID", "Priority", "Arrival", "Burst"] + [str(i) for i in range(1, 33)]
        self.timeline_grid.setHorizontalHeaderLabels(headers)
        self.timeline_grid.setColumnWidth(0, 70)
        self.timeline_grid.setColumnWidth(1, 55)
        self.timeline_grid.setColumnWidth(2, 55)
        self.timeline_grid.setColumnWidth(3, 45)
        for i in range(4, 36):
            self.timeline_grid.setColumnWidth(i, 35)
        self.timeline_grid.verticalHeader().setDefaultSectionSize(30)
        self.timeline_grid.verticalHeader().hide()
        self.timeline_grid.cellChanged.connect(self._on_table_cell_changed)
        self._setup_timeline_grid()
        layout.addWidget(self.timeline_grid)
        
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
        desc_scroll.setMinimumHeight(120)
        desc_scroll.setMaximumHeight(200)
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
        """Fill the unified table with current process data (cols 0-3)"""
        self._updating_table = True
        for i, proc in enumerate(self.processes):
            id_item = QTableWidgetItem(proc["id"])
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            id_item.setTextAlignment(Qt.AlignCenter)
            self.timeline_grid.setItem(i, 0, id_item)
            
            priority_item = QTableWidgetItem(str(proc["priority"]))
            priority_item.setTextAlignment(Qt.AlignCenter)
            self.timeline_grid.setItem(i, 1, priority_item)
            
            arrival_item = QTableWidgetItem(str(proc["arrival"]))
            arrival_item.setTextAlignment(Qt.AlignCenter)
            self.timeline_grid.setItem(i, 2, arrival_item)
            
            burst_item = QTableWidgetItem(str(proc["burst"]))
            burst_item.setTextAlignment(Qt.AlignCenter)
            self.timeline_grid.setItem(i, 3, burst_item)
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
        """Initialize the timeline portion of the grid (cols 4-35)"""
        self._updating_table = True
        for i in range(4):
            for j in range(4, 36):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(Qt.white)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.timeline_grid.setItem(i, j, item)
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
        
        self._update_timeline(step["timeline"], step["rs_markers"])
    
    def _update_timeline(self, timeline_data, rs_markers):
        """Update the timeline grid based on step data (cols 4-35)"""
        if not self.timeline_grid:
            return
            
        process_to_row = {proc["id"]: i for i, proc in enumerate(self.processes[:4])}
        
        for row in range(4):
            for col in range(4, 36):
                item = self.timeline_grid.item(row, col)
                if item:
                    item.setBackground(Qt.white)
                    item.setText("")
                    item.setForeground(QColor(0, 0, 0))
        
        for process_id, times in timeline_data.items():
            row = process_to_row.get(process_id)
            if row is not None:
                for t in times:
                    if 1 <= t <= 32:
                        col = t + 3
                        item = self.timeline_grid.item(row, col)
                        if item:
                            item.setBackground(self.scheduling_block_color)
                            item.setText("-")
                            item.setForeground(QColor(0, 0, 0))
        
        for process_id, times in rs_markers.items():
            row = process_to_row.get(process_id)
            if row is not None:
                for t in times:
                    if 1 <= t <= 32:
                        col = t + 3
                        item = self.timeline_grid.item(row, col)
                        if item:
                            current_text = item.text()
                            if current_text and current_text != "":
                                item.setText(f"{current_text}\nRS")
                            else:
                                item.setText("RS")
                            item.setForeground(QColor(128, 128, 128))
    
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
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            self._update_timeline(step["timeline"], step["rs_markers"])
    
    def apply_theme(self, theme: dict):
        """Apply theme colors to the tutorial page"""
        self.current_theme = theme
        
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
        
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            self._update_timeline(step["timeline"], step["rs_markers"])
