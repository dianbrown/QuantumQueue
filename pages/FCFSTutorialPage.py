"""
FCFS Tutorial Page - Step-by-step walkthrough of First Come First Served algorithm
Supports multiple problem sets with dropdown selector
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                              QLabel, QTableWidget, QTableWidgetItem, QFrame,
                              QScrollArea, QHeaderView, QComboBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont


class FCFSTutorialPage(QWidget):
    """Step-by-step FCFS algorithm tutorial page with multiple problem sets"""
    
    # Signal to navigate back to help page
    back_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_step = 0
        self.current_set_index = 0
        self.current_theme = {}
        self.scheduling_block_color = QColor("#ffff00")  # Default yellow
        
        # Define all problem sets
        self.problem_sets = self._create_problem_sets()
        
        # Current problem set
        self.processes = self.problem_sets[0]["processes"]
        self.steps = self.problem_sets[0]["steps"]
        
        self.setup_ui()
        self._show_step(0)
    
    def _create_problem_sets(self):
        """Create all problem sets with their steps"""
        return [
            self._create_set_1(),
            self._create_set_2(),
            self._create_set_3(),
        ]
    
    def _create_set_1(self):
        """Problem Set 1: Original set"""
        processes = [
            {"id": "A", "priority": 4, "arrival": 11, "burst": 8},
            {"id": "B", "priority": 1, "arrival": 13, "burst": 9},
            {"id": "C", "priority": 2, "arrival": 6, "burst": 9},
            {"id": "D", "priority": 3, "arrival": 1, "burst": 6},
        ]
        
        # FCFS sorted order: by (arrival, id) -> D(1), C(6), A(11), B(13)
        steps = [
            {
                "title": "Step 0: Initial State",
                "description": (
                    "FCFS (First Come First Served) is a non-preemptive scheduling algorithm.\n\n"
                    "Core Rules:\n"
                    "- Processes execute in the order they arrive\n"
                    "- Once a process starts, it runs to completion\n"
                    "- Tie-breaker: Process ID (alphabetical order)\n\n"
                    "Our problem set has 4 processes: A, B, C, D with different arrival times."
                ),
                "timeline": {},
                "rs_markers": {}
            },
            {
                "title": "Step 1: Sort by Arrival Time",
                "description": (
                    "First, sort all processes by arrival time. If arrivals are equal, use Process ID.\n\n"
                    "Sorted order: D(1) -> C(6) -> A(11) -> B(13)\n\n"
                    "RS (Ready State) markers show when each process enters the ready queue.\n"
                    "This is always the first step - mark the arrival times on the timeline."
                ),
                "timeline": {},
                "rs_markers": {
                    "D": [1],
                    "C": [6],
                    "A": [11],
                    "B": [13],
                }
            },
            {
                "title": "Step 2: Execute Process D",
                "description": (
                    "Process D arrives first at t=1 and has burst time of 6.\n\n"
                    "Since FCFS is non-preemptive, D runs from t=1 to t=6 (6 time units).\n\n"
                    "D completes at t=7 (end time = start + burst = 1 + 6 = 7)."
                ),
                "timeline": {
                    "D": list(range(1, 7)),
                },
                "rs_markers": {
                    "D": [1],
                    "C": [6],
                    "A": [11],
                    "B": [13],
                }
            },
            {
                "title": "Step 3: Execute Process C",
                "description": (
                    "Process C arrived at t=6 (while D was still running).\n\n"
                    "D finishes at t=7, so C starts immediately at t=7.\n"
                    "C has burst time of 9, so it runs from t=7 to t=15.\n\n"
                    "Note: Even though C arrived at t=6, it had to wait for D to complete."
                ),
                "timeline": {
                    "D": list(range(1, 7)),
                    "C": list(range(7, 16)),
                },
                "rs_markers": {
                    "D": [1],
                    "C": [6],
                    "A": [11],
                    "B": [13],
                }
            },
            {
                "title": "Step 4: Execute Process A",
                "description": (
                    "Process A arrived at t=11 (while C was running).\n\n"
                    "C finishes at t=16, so A starts at t=16.\n"
                    "A has burst time of 8, so it runs from t=16 to t=23.\n\n"
                    "A waited from t=11 to t=16 (waiting time = 5)."
                ),
                "timeline": {
                    "D": list(range(1, 7)),
                    "C": list(range(7, 16)),
                    "A": list(range(16, 24)),
                },
                "rs_markers": {
                    "D": [1],
                    "C": [6],
                    "A": [11],
                    "B": [13],
                }
            },
            {
                "title": "Step 5: Execute Process B",
                "description": (
                    "Process B arrived at t=13 (while C was still running).\n\n"
                    "A finishes at t=24, so B starts at t=24.\n"
                    "B has burst time of 9, so it runs from t=24 to t=32.\n\n"
                    "B waited from t=13 to t=24 (waiting time = 11)."
                ),
                "timeline": {
                    "D": list(range(1, 7)),
                    "C": list(range(7, 16)),
                    "A": list(range(16, 24)),
                    "B": list(range(24, 33)),
                },
                "rs_markers": {
                    "D": [1],
                    "C": [6],
                    "A": [11],
                    "B": [13],
                }
            },
            {
                "title": "Step 6: Final Solution",
                "description": (
                    "FCFS Scheduling Complete!\n\n"
                    "Execution Order: D -> C -> A -> B\n\n"
                    "Metrics:\n"
                    "- Process D: Start=1, End=7, TAT=6, WT=0\n"
                    "- Process C: Start=7, End=16, TAT=10, WT=1\n"
                    "- Process A: Start=16, End=24, TAT=13, WT=5\n"
                    "- Process B: Start=24, End=32 (truncated), TAT=19, WT=11\n\n"
                    "Average Waiting Time: (0+1+5+11)/4 = 4.25\n"
                    "Average Turnaround Time: (6+10+13+19)/4 = 12.0"
                ),
                "timeline": {
                    "D": list(range(1, 7)),
                    "C": list(range(7, 16)),
                    "A": list(range(16, 24)),
                    "B": list(range(24, 33)),
                },
                "rs_markers": {
                    "D": [1],
                    "C": [6],
                    "A": [11],
                    "B": [13],
                }
            },
        ]
        
        return {"name": "FCFS Tutorial 1", "processes": processes, "steps": steps}
    
    def _create_set_2(self):
        """Problem Set 2: Second set from user's image"""
        processes = [
            {"id": "A", "priority": 4, "arrival": 27, "burst": 4},
            {"id": "B", "priority": 1, "arrival": 9, "burst": 8},
            {"id": "C", "priority": 1, "arrival": 19, "burst": 7},
            {"id": "D", "priority": 2, "arrival": 1, "burst": 13},
        ]
        
        # FCFS sorted order: by (arrival, id) -> D(1), B(9), C(19), A(27)
        steps = [
            {
                "title": "Step 0: Initial State",
                "description": (
                    "FCFS (First Come First Served) is a non-preemptive scheduling algorithm.\n\n"
                    "Core Rules:\n"
                    "- Processes execute in the order they arrive\n"
                    "- Once a process starts, it runs to completion\n"
                    "- Tie-breaker: Process ID (alphabetical order)\n\n"
                    "Our problem set has 4 processes: A, B, C, D with different arrival times."
                ),
                "timeline": {},
                "rs_markers": {}
            },
            {
                "title": "Step 1: Sort by Arrival Time",
                "description": (
                    "First, sort all processes by arrival time. If arrivals are equal, use Process ID.\n\n"
                    "Sorted order: D(1) -> B(9) -> C(19) -> A(27)\n\n"
                    "RS (Ready State) markers show when each process enters the ready queue.\n"
                    "This is always the first step - mark the arrival times on the timeline."
                ),
                "timeline": {},
                "rs_markers": {
                    "D": [1],
                    "B": [9],
                    "C": [19],
                    "A": [27],
                }
            },
            {
                "title": "Step 2: Execute Process D",
                "description": (
                    "Process D arrives first at t=1 and has burst time of 13.\n\n"
                    "Since FCFS is non-preemptive, D runs from t=1 to t=13 (13 time units).\n\n"
                    "D completes at t=14 (end time = start + burst = 1 + 13 = 14)."
                ),
                "timeline": {
                    "D": list(range(1, 14)),
                },
                "rs_markers": {
                    "D": [1],
                    "B": [9],
                    "C": [19],
                    "A": [27],
                }
            },
            {
                "title": "Step 3: Execute Process B",
                "description": (
                    "Process B arrived at t=9 (while D was running).\n\n"
                    "D finishes at t=14, so B starts at t=14.\n"
                    "B has burst time of 8, so it runs from t=14 to t=21.\n\n"
                    "B waited from t=9 to t=14 (waiting time = 5)."
                ),
                "timeline": {
                    "D": list(range(1, 14)),
                    "B": list(range(14, 22)),
                },
                "rs_markers": {
                    "D": [1],
                    "B": [9],
                    "C": [19],
                    "A": [27],
                }
            },
            {
                "title": "Step 4: Execute Process C",
                "description": (
                    "Process C arrived at t=19 (while B was running).\n\n"
                    "B finishes at t=22, so C starts at t=22.\n"
                    "C has burst time of 7, so it runs from t=22 to t=28.\n\n"
                    "C waited from t=19 to t=22 (waiting time = 3)."
                ),
                "timeline": {
                    "D": list(range(1, 14)),
                    "B": list(range(14, 22)),
                    "C": list(range(22, 29)),
                },
                "rs_markers": {
                    "D": [1],
                    "B": [9],
                    "C": [19],
                    "A": [27],
                }
            },
            {
                "title": "Step 5: Execute Process A",
                "description": (
                    "Process A arrived at t=27 (while C was running).\n\n"
                    "C finishes at t=29, so A starts at t=29.\n"
                    "A has burst time of 4, so it runs from t=29 to t=32.\n\n"
                    "A waited from t=27 to t=29 (waiting time = 2)."
                ),
                "timeline": {
                    "D": list(range(1, 14)),
                    "B": list(range(14, 22)),
                    "C": list(range(22, 29)),
                    "A": list(range(29, 33)),
                },
                "rs_markers": {
                    "D": [1],
                    "B": [9],
                    "C": [19],
                    "A": [27],
                }
            },
            {
                "title": "Step 6: Final Solution",
                "description": (
                    "FCFS Scheduling Complete!\n\n"
                    "Execution Order: D -> B -> C -> A\n\n"
                    "Metrics:\n"
                    "- Process D: Start=1, End=14, TAT=13, WT=0\n"
                    "- Process B: Start=14, End=22, TAT=13, WT=5\n"
                    "- Process C: Start=22, End=29, TAT=10, WT=3\n"
                    "- Process A: Start=29, End=32 (truncated), TAT=5, WT=2\n\n"
                    "Average Waiting Time: (0+5+3+2)/4 = 2.5\n"
                    "Average Turnaround Time: (13+13+10+5)/4 = 10.25"
                ),
                "timeline": {
                    "D": list(range(1, 14)),
                    "B": list(range(14, 22)),
                    "C": list(range(22, 29)),
                    "A": list(range(29, 33)),
                },
                "rs_markers": {
                    "D": [1],
                    "B": [9],
                    "C": [19],
                    "A": [27],
                }
            },
        ]
        
        return {"name": "FCFS Tutorial 2", "processes": processes, "steps": steps}
    
    def _create_set_3(self):
        """Problem Set 3: Third set from user's image"""
        processes = [
            {"id": "A", "priority": 4, "arrival": 5, "burst": 5},
            {"id": "B", "priority": 1, "arrival": 9, "burst": 8},
            {"id": "C", "priority": 3, "arrival": 3, "burst": 7},
            {"id": "D", "priority": 2, "arrival": 1, "burst": 11},
        ]
        
        # FCFS sorted order: by (arrival, id) -> D(1), C(3), A(5), B(9)
        steps = [
            {
                "title": "Step 0: Initial State",
                "description": (
                    "FCFS (First Come First Served) is a non-preemptive scheduling algorithm.\n\n"
                    "Core Rules:\n"
                    "- Processes execute in the order they arrive\n"
                    "- Once a process starts, it runs to completion\n"
                    "- Tie-breaker: Process ID (alphabetical order)\n\n"
                    "Our problem set has 4 processes: A, B, C, D with different arrival times."
                ),
                "timeline": {},
                "rs_markers": {}
            },
            {
                "title": "Step 1: Sort by Arrival Time",
                "description": (
                    "First, sort all processes by arrival time. If arrivals are equal, use Process ID.\n\n"
                    "Sorted order: D(1) -> C(3) -> A(5) -> B(9)\n\n"
                    "RS (Ready State) markers show when each process enters the ready queue.\n"
                    "This is always the first step - mark the arrival times on the timeline."
                ),
                "timeline": {},
                "rs_markers": {
                    "D": [1],
                    "C": [3],
                    "A": [5],
                    "B": [9],
                }
            },
            {
                "title": "Step 2: Execute Process D",
                "description": (
                    "Process D arrives first at t=1 and has burst time of 11.\n\n"
                    "Since FCFS is non-preemptive, D runs from t=1 to t=11 (11 time units).\n\n"
                    "D completes at t=12 (end time = start + burst = 1 + 11 = 12)."
                ),
                "timeline": {
                    "D": list(range(1, 12)),
                },
                "rs_markers": {
                    "D": [1],
                    "C": [3],
                    "A": [5],
                    "B": [9],
                }
            },
            {
                "title": "Step 3: Execute Process C",
                "description": (
                    "Process C arrived at t=3 (while D was running).\n\n"
                    "D finishes at t=12, so C starts at t=12.\n"
                    "C has burst time of 7, so it runs from t=12 to t=18.\n\n"
                    "C waited from t=3 to t=12 (waiting time = 9)."
                ),
                "timeline": {
                    "D": list(range(1, 12)),
                    "C": list(range(12, 19)),
                },
                "rs_markers": {
                    "D": [1],
                    "C": [3],
                    "A": [5],
                    "B": [9],
                }
            },
            {
                "title": "Step 4: Execute Process A",
                "description": (
                    "Process A arrived at t=5 (while D was running).\n\n"
                    "C finishes at t=19, so A starts at t=19.\n"
                    "A has burst time of 5, so it runs from t=19 to t=23.\n\n"
                    "A waited from t=5 to t=19 (waiting time = 14)."
                ),
                "timeline": {
                    "D": list(range(1, 12)),
                    "C": list(range(12, 19)),
                    "A": list(range(19, 24)),
                },
                "rs_markers": {
                    "D": [1],
                    "C": [3],
                    "A": [5],
                    "B": [9],
                }
            },
            {
                "title": "Step 5: Execute Process B",
                "description": (
                    "Process B arrived at t=9 (while D was running).\n\n"
                    "A finishes at t=24, so B starts at t=24.\n"
                    "B has burst time of 8, so it runs from t=24 to t=31.\n\n"
                    "B waited from t=9 to t=24 (waiting time = 15)."
                ),
                "timeline": {
                    "D": list(range(1, 12)),
                    "C": list(range(12, 19)),
                    "A": list(range(19, 24)),
                    "B": list(range(24, 32)),
                },
                "rs_markers": {
                    "D": [1],
                    "C": [3],
                    "A": [5],
                    "B": [9],
                }
            },
            {
                "title": "Step 6: Final Solution",
                "description": (
                    "FCFS Scheduling Complete!\n\n"
                    "Execution Order: D -> C -> A -> B\n\n"
                    "Metrics:\n"
                    "- Process D: Start=1, End=12, TAT=11, WT=0\n"
                    "- Process C: Start=12, End=19, TAT=16, WT=9\n"
                    "- Process A: Start=19, End=24, TAT=19, WT=14\n"
                    "- Process B: Start=24, End=32, TAT=23, WT=15\n\n"
                    "Average Waiting Time: (0+9+14+15)/4 = 9.5\n"
                    "Average Turnaround Time: (11+16+19+23)/4 = 17.25"
                ),
                "timeline": {
                    "D": list(range(1, 12)),
                    "C": list(range(12, 19)),
                    "A": list(range(19, 24)),
                    "B": list(range(24, 32)),
                },
                "rs_markers": {
                    "D": [1],
                    "C": [3],
                    "A": [5],
                    "B": [9],
                }
            },
        ]
        
        return {"name": "FCFS Tutorial 3", "processes": processes, "steps": steps}
    
    def setup_ui(self):
        """Setup the tutorial UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Top row: Back button and Problem Set selector
        top_layout = QHBoxLayout()
        
        self.back_btn = QPushButton("Back to Help")
        self.back_btn.setObjectName("backBtn")
        self.back_btn.setMaximumWidth(150)
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.clicked.connect(self.back_requested.emit)
        top_layout.addWidget(self.back_btn)
        
        top_layout.addStretch()
        
        # Problem set selector
        selector_label = QLabel("Problem Set:")
        selector_label.setObjectName("selectorLabel")
        top_layout.addWidget(selector_label)
        
        self.set_selector = QComboBox()
        self.set_selector.setObjectName("setSelector")
        self.set_selector.setMinimumWidth(180)
        for ps in self.problem_sets:
            self.set_selector.addItem(ps["name"])
        self.set_selector.currentIndexChanged.connect(self._on_set_changed)
        top_layout.addWidget(self.set_selector)
        
        layout.addLayout(top_layout)
        
        # Title
        self.page_title = QLabel(self.problem_sets[0]["name"])
        self.page_title.setObjectName("tutorialTitle")
        layout.addWidget(self.page_title)
        
        # Process table
        self.process_table = QTableWidget(4, 4)
        self.process_table.setHorizontalHeaderLabels(["Process ID", "Priority", "Arrival", "Burst time"])
        self.process_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.process_table.setMaximumHeight(170)
        self._populate_process_table()
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
    
    def _on_set_changed(self, index):
        """Handle problem set selection change"""
        self.current_set_index = index
        self.processes = self.problem_sets[index]["processes"]
        self.steps = self.problem_sets[index]["steps"]
        
        # Update title
        self.page_title.setText(self.problem_sets[index]["name"])
        
        # Refresh tables
        self._populate_process_table()
        self._setup_timeline_grid()
        
        # Reset to first step
        self.current_step = 0
        self._show_step(0)
    
    def _populate_process_table(self):
        """Fill the process table with current problem set data"""
        for i, proc in enumerate(self.processes):
            self.process_table.setItem(i, 0, QTableWidgetItem(proc["id"]))
            self.process_table.setItem(i, 1, QTableWidgetItem(str(proc["priority"])))
            self.process_table.setItem(i, 2, QTableWidgetItem(str(proc["arrival"])))
            self.process_table.setItem(i, 3, QTableWidgetItem(str(proc["burst"])))
    
    def _setup_timeline_grid(self):
        """Initialize the timeline grid with process IDs"""
        for i, proc in enumerate(self.processes):
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
        # Skip if timeline grid is not visible or not fully initialized
        if not self.timeline_grid or not self.timeline_grid.isVisible():
            return
            
        # Create process ID to row mapping
        process_to_row = {proc["id"]: i for i, proc in enumerate(self.processes)}
        
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
            
            QLabel#selectorLabel {{
                font-size: 14px;
                color: {text_color};
                background-color: transparent;
            }}
            
            QComboBox#setSelector {{
                background-color: {input_bg};
                border: 1px solid {table_grid};
                padding: 8px 12px;
                border-radius: 6px;
                color: {text_color};
                font-size: 14px;
            }}
            
            QComboBox#setSelector:hover {{
                border: 1px solid {button_bg};
            }}
            
            QComboBox#setSelector::drop-down {{
                border: none;
                padding-right: 10px;
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
