"""Main window for the CPU Scheduling application."""

from typing import List, Optional
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QComboBox, QLabel,
    QHeaderView, QMessageBox, QSpinBox, QMenu, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

from CPU.models.process import Process
from CPU.models.scheduling_result import SchedulingResult
from CPU.algorithms import FCFSScheduler, FCFSPriorityScheduler, RoundRobinScheduler, RoundRobinPriorityScheduler, SJFScheduler, SJFPriorityScheduler, SRTScheduler
from CPU.utils.process_generator import ProcessGenerator


class CPUSchedulingApp(QMainWindow):
    """Main application window for CPU Scheduling practice."""
    
    def __init__(self):
        super().__init__()
        self.processes: List[Process] = []
        self.timeline_grid: Optional[QTableWidget] = None
        self.process_table: Optional[QTableWidget] = None
        self.current_schedule: List[Optional[str]] = []
        self.solution_result: Optional[SchedulingResult] = None
        self.is_locked = False
        self.results_label: Optional[QLabel] = None
        self.results_scroll_area: Optional[QScrollArea] = None
        self.algorithm_name_label: Optional[QLabel] = None
        self.quantum_spinbox: Optional[QSpinBox] = None
        self.rs_markers = {}  # Track RS markers: {(row, col): True}
        
        # Initialize schedulers
        self.schedulers = {
            "FCFS": FCFSScheduler(),
            "FCFS with Priority": FCFSPriorityScheduler(higher_is_better=True),
            "SJF": SJFScheduler(),
            "SJF Priority": SJFPriorityScheduler(),
            "SRT": SRTScheduler(),
            "Round Robin": RoundRobinScheduler(2),
            "Round Robin with Priority": RoundRobinPriorityScheduler(2)
        }
        
        # Default scheduling block color (yellow)
        self.scheduling_block_color = QColor("#ffff00")
        
        self.init_ui()
        self.add_sample_processes()
        self.update_timeline_grid()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("CPU Scheduling Practice App")
        self.setGeometry(100, 100, 1200, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Top controls
        controls_layout = QHBoxLayout()
        
        # Algorithm dropdown
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(list(self.schedulers.keys()))
        self.algorithm_combo.setMinimumWidth(300)
        self.algorithm_combo.setStyleSheet("""
            QComboBox {
                font-size: 13px;
                padding: 6px;
            }
        """)
        self.algorithm_combo.currentTextChanged.connect(self.on_algorithm_changed)
        controls_layout.addWidget(QLabel("Algorithm:"))
        controls_layout.addWidget(self.algorithm_combo)
        
        # Quantum input (for Round Robin algorithms)
        self.quantum_spinbox = QSpinBox()
        self.quantum_spinbox.setMinimum(1)
        self.quantum_spinbox.setMaximum(10)
        self.quantum_spinbox.setValue(2)
        self.quantum_spinbox.valueChanged.connect(self.on_quantum_changed)
        self.quantum_label = QLabel("Quantum:")
        controls_layout.addWidget(self.quantum_label)
        controls_layout.addWidget(self.quantum_spinbox)
        
        # Initially hide quantum controls
        self.quantum_label.setVisible(False)
        self.quantum_spinbox.setVisible(False)
        
        controls_layout.addStretch()
        main_layout.addLayout(controls_layout)
        
        # Main content layout
        content_layout = QHBoxLayout()
        
        # Left panel - Process input table
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Process Input:"))
        
        self.setup_process_table()
        left_panel.addWidget(self.process_table)
        
        # Process control buttons
        process_controls = QHBoxLayout()
        process_controls.setSpacing(5)  # Reduce spacing between buttons
        
        add_btn = QPushButton("Add Process")
        add_btn.clicked.connect(self.add_process)
        add_btn.setMinimumWidth(80)  # Set minimum width
        
        delete_btn = QPushButton("Delete Process")
        delete_btn.clicked.connect(self.delete_process)
        delete_btn.setMinimumWidth(90)  # Set minimum width
        
        randomize_btn = QPushButton("Randomize")
        randomize_btn.clicked.connect(self.randomize_processes)
        randomize_btn.setMinimumWidth(75)  # Set minimum width
        
        process_controls.addWidget(add_btn)
        process_controls.addWidget(delete_btn)
        process_controls.addWidget(randomize_btn)
        left_panel.addLayout(process_controls)
        
        # Solution control buttons
        solution_controls = QHBoxLayout()
        check_btn = QPushButton("Check Solution")
        check_btn.clicked.connect(self.check_solution)
        show_btn = QPushButton("Show Solution")
        show_btn.clicked.connect(self.show_solution)
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_grid)
        
        solution_controls.addWidget(check_btn)
        solution_controls.addWidget(show_btn)
        solution_controls.addWidget(reset_btn)
        left_panel.addLayout(solution_controls)
        
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        left_widget.setFixedWidth(380)  # Increased from 300 to 380 pixels
        content_layout.addWidget(left_widget)
        
        # Center panel - Timeline grid
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("Timeline Grid:"))
        
        self.setup_timeline_grid()
        right_panel.addWidget(self.timeline_grid)
        
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
        self.results_scroll_area.setMinimumHeight(150)
        self.results_scroll_area.setMaximumHeight(200)
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

    def setup_process_table(self):
        """Set up the process input table."""
        self.process_table = QTableWidget(0, 4)
        self.process_table.setHorizontalHeaderLabels(["Process ID", "Priority", "Arrival", "Burst time"])
        self.process_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def setup_timeline_grid(self):
        """Set up the timeline grid for visualization."""
        self.timeline_grid = QTableWidget(0, 33)
        
        # Set up headers
        headers = ["Process ID"] + [str(i) for i in range(1, 33)]
        self.timeline_grid.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        self.timeline_grid.setColumnWidth(0, 80)
        for i in range(1, 33):
            self.timeline_grid.setColumnWidth(i, 35)  # Increased from 30 to 35 to fit "RS" text
        
        # Connect cell events
        self.timeline_grid.cellClicked.connect(self.on_cell_clicked)
        self.timeline_grid.cellEntered.connect(self.on_cell_hover)
        
        # Enable context menu
        self.timeline_grid.setContextMenuPolicy(Qt.CustomContextMenu)
        self.timeline_grid.customContextMenuRequested.connect(self.show_context_menu)
        self.timeline_grid.cellDoubleClicked.connect(self.on_cell_double_clicked)
        
        # Enable mouse tracking for better responsiveness
        self.timeline_grid.setMouseTracking(True)
        
        # Set row height
        self.timeline_grid.verticalHeader().setDefaultSectionSize(30)
        self.timeline_grid.verticalHeader().hide()

    def set_scheduling_block_color(self, color):
        """Set the color for scheduling blocks in the timeline grid."""
        old_color = self.scheduling_block_color
        self.scheduling_block_color = QColor(color)
        # Refresh all existing colored blocks with the new color
        self.refresh_colored_blocks(old_color)

    def refresh_colored_blocks(self, old_color):
        """Refresh all colored blocks in the timeline grid with the new color."""
        if not self.timeline_grid:
            return
            
        # Iterate through all cells in the timeline grid
        for row in range(self.timeline_grid.rowCount()):
            for col in range(1, self.timeline_grid.columnCount()):  # Skip process ID column
                item = self.timeline_grid.item(row, col)
                if item:
                    # Check if this cell was colored with the old scheduling color
                    # We check both the old color and common scheduling block indicators
                    item_color = item.background().color()
                    item_text = item.text()
                    
                    # If the cell has the old scheduling color or contains a dash (scheduling block marker)
                    # and is not white, update it to the new color
                    if (item_color.name().lower() == old_color.name().lower() or 
                        (item_text in ["-", "-\nRS"] and item_color != Qt.white)):
                        item.setBackground(self.scheduling_block_color)

    def add_sample_processes(self):
        """Add sample processes for demonstration."""
        sample_processes = [
            Process("A", 4, 11, 8),
            Process("B", 1, 13, 9),
            Process("C", 2, 6, 9),
            Process("D", 3, 1, 6)
        ]
        self.processes = sample_processes
        self.update_process_table()

    def update_process_table(self):
        """Update the process table with current processes."""
        self.process_table.setRowCount(len(self.processes))
        for i, process in enumerate(self.processes):
            self.process_table.setItem(i, 0, QTableWidgetItem(process.id))
            self.process_table.setItem(i, 1, QTableWidgetItem(str(process.priority)))
            self.process_table.setItem(i, 2, QTableWidgetItem(str(process.arrival)))
            self.process_table.setItem(i, 3, QTableWidgetItem(str(process.burst)))

    def update_timeline_grid(self):
        """Update the timeline grid with current processes."""
        if not self.processes:
            self.timeline_grid.setRowCount(0)
            return
            
        # Save current RS markers
        old_rs_markers = self.rs_markers.copy()
        
        # Clear all existing cells first
        for i in range(self.timeline_grid.rowCount()):
            for j in range(1, self.timeline_grid.columnCount()):
                item = self.timeline_grid.item(i, j)
                if item:
                    item.setBackground(Qt.white)
                    item.setText("")
        
        self.timeline_grid.setRowCount(len(self.processes))
        
        for i, process in enumerate(self.processes):
            # Process ID column
            item = QTableWidgetItem(process.id)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item.setTextAlignment(Qt.AlignCenter)
            self.timeline_grid.setItem(i, 0, item)
            
            # Timeline columns - create fresh cells
            for j in range(1, 33):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(Qt.white)  # Ensure white background
                if not self.is_locked:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.timeline_grid.setItem(i, j, item)
        
        # Restore RS markers
        self.rs_markers = old_rs_markers
        for (row, col) in self.rs_markers:
            if row < self.timeline_grid.rowCount() and col < self.timeline_grid.columnCount():
                self.update_cell_display(row, col)

    def on_cell_clicked(self, row: int, col: int):
        """Handle cell click events."""
        if col == 0 or self.is_locked:
            return
            
        item = self.timeline_grid.item(row, col)
        if item is None:
            return
            
        # Clear all other cells in this column first
        for r in range(self.timeline_grid.rowCount()):
            other_item = self.timeline_grid.item(r, col)
            if other_item and r != row:
                other_item.setBackground(Qt.white)
                other_item.setForeground(QColor(0, 0, 0))  # Black text
                # Handle RS marker preservation when clearing
                if (r, col) in self.rs_markers:
                    other_item.setText("RS")
                    other_item.setForeground(QColor(128, 128, 128))  # Gray for RS
                else:
                    other_item.setText("")
        
        # Toggle current cell
        if item.background().color().name().lower() == self.scheduling_block_color.name().lower():
            item.setBackground(Qt.white)
            item.setForeground(QColor(0, 0, 0))  # Black text
            # Handle RS marker preservation when turning off scheduling block
            if (row, col) in self.rs_markers:
                item.setText("RS")
                item.setForeground(QColor(128, 128, 128))  # Gray for RS
            else:
                item.setText("")
        else:
            item.setBackground(self.scheduling_block_color)
            item.setForeground(QColor(0, 0, 0))  # Black text
            # Handle RS marker preservation when turning on scheduling block
            if (row, col) in self.rs_markers:
                item.setText("-\nRS")
            else:
                item.setText("-")

    def on_cell_hover(self, row: int, col: int):
        """Handle cell hover events."""
        if col == 0 or self.is_locked:
            return
        # Could add hover effects here if needed

    def on_cell_double_clicked(self, row: int, col: int):
        """Handle cell double-click events."""
        if col == 0 or self.is_locked:
            return
            
        # Double-click fills multiple consecutive cells for the process
        item = self.timeline_grid.item(row, col)
        if item is None:
            return
            
        # Clear all cells in this column first
        for r in range(self.timeline_grid.rowCount()):
            other_item = self.timeline_grid.item(r, col)
            if other_item:
                other_item.setBackground(Qt.white)
                other_item.setText("")
        
        # Find the process burst time and fill consecutive cells
        process_id = self.timeline_grid.item(row, 0).text()
        process = next((p for p in self.processes if p.id == process_id), None)
        
        if process:
            # Fill burst_time number of cells starting from clicked column
            for i in range(process.burst):
                if col + i < self.timeline_grid.columnCount():
                    cell_item = self.timeline_grid.item(row, col + i)
                    if cell_item:
                        # Clear other processes in this column
                        for r in range(self.timeline_grid.rowCount()):
                            if r != row:
                                other_item = self.timeline_grid.item(r, col + i)
                                if other_item:
                                    other_item.setBackground(Qt.white)
                                    other_item.setText("")
                        
                        cell_item.setBackground(self.scheduling_block_color)
                        cell_item.setText("-")

    def show_context_menu(self, position):
        """Show context menu for RS markers."""
        item = self.timeline_grid.itemAt(position)
        if item is None:
            return
            
        row = item.row()
        col = item.column()
        
        # Only allow RS markers in timeline columns (not process ID column)
        if col == 0:
            return
            
        menu = QMenu(self)
        
        # Check if RS marker exists at this position
        has_rs_marker = (row, col) in self.rs_markers
        
        if has_rs_marker:
            action = menu.addAction("Remove RS Marker")
            action.triggered.connect(lambda: self.remove_rs_marker(row, col))
        else:
            action = menu.addAction("Add RS Marker")
            action.triggered.connect(lambda: self.add_rs_marker(row, col))
            
        menu.exec(self.timeline_grid.mapToGlobal(position))

    def add_rs_marker(self, row: int, col: int):
        """Add RS marker to a cell."""
        # Remove any existing RS marker in this row (only one per process)
        self.remove_rs_markers_in_row(row)
        
        # Add new RS marker
        self.rs_markers[(row, col)] = True
        self.update_cell_display(row, col)

    def remove_rs_marker(self, row: int, col: int):
        """Remove RS marker from a cell."""
        if (row, col) in self.rs_markers:
            del self.rs_markers[(row, col)]
            self.update_cell_display(row, col)

    def remove_rs_markers_in_row(self, row: int):
        """Remove all RS markers in a specific row (process)."""
        markers_to_remove = [(r, c) for r, c in self.rs_markers.keys() if r == row]
        for r, c in markers_to_remove:
            del self.rs_markers[(r, c)]
            self.update_cell_display(r, c)

    def update_cell_display(self, row: int, col: int):
        """Update cell display to show/hide RS marker."""
        item = self.timeline_grid.item(row, col)
        if item is None:
            return
            
        has_rs_marker = (row, col) in self.rs_markers
        current_text = item.text()
        
        if has_rs_marker:
            # Add RS marker as overlay text (keep existing content)
            if current_text and current_text != "" and "RS" not in current_text:
                item.setText(f"{current_text}\nRS")
            else:
                item.setText("RS")
            # Set light gray color for RS text
            item.setForeground(QColor(128, 128, 128))
        else:
            # Remove RS marker but keep other content
            if current_text and "RS" in current_text:
                new_text = current_text.replace("\nRS", "").replace("RS", "")
                item.setText(new_text)
            # Reset text color to black
            item.setForeground(QColor(0, 0, 0))

    def on_algorithm_changed(self):
        """Handle algorithm selection change."""
        algorithm = self.algorithm_combo.currentText()
        
        # Show/hide quantum controls for Round Robin algorithms
        is_round_robin = "Round Robin" in algorithm
        self.quantum_label.setVisible(is_round_robin)
        self.quantum_spinbox.setVisible(is_round_robin)
        
        # Update scheduler with current quantum if needed
        if is_round_robin:
            self.update_round_robin_scheduler()
        
        self.reset_grid()
    
    def on_quantum_changed(self):
        """Handle quantum value change."""
        self.update_round_robin_scheduler()
        self.reset_grid()
    
    def update_round_robin_scheduler(self):
        """Update Round Robin schedulers with current quantum value."""
        quantum = self.quantum_spinbox.value()
        self.schedulers["Round Robin"] = RoundRobinScheduler(quantum)
        self.schedulers["Round Robin with Priority"] = RoundRobinPriorityScheduler(quantum)

    def add_process(self):
        """Add a new process."""
        next_id = chr(ord('A') + len(self.processes))
        new_process = Process(next_id, 1, 1, 1)  # Start arrival at 1 instead of 0
        self.processes.append(new_process)
        
        # Clear solution state
        self.solution_result = None
        self.current_schedule = []
        self.is_locked = False
        
        self.update_process_table()
        self.update_timeline_grid()
        if self.results_label:
            self.results_label.setText("")

    def delete_process(self):
        """Delete the last process."""
        if self.processes:
            self.processes.pop()
            
            # Clear solution state
            self.solution_result = None
            self.current_schedule = []
            self.is_locked = False
            
            self.update_process_table()
            self.update_timeline_grid()
            if self.results_label:
                self.results_label.setText("")

    def randomize_processes(self):
        """Generate random processes."""
        # Check if current algorithm needs unique arrival times
        algorithm = self.algorithm_combo.currentText()
        
        # Only basic FCFS and Round Robin need unique arrivals (no priority variants)
        algorithms_needing_unique_arrivals = ["FCFS", "Round Robin (Q="]
        
        # Use unique arrivals only for pure FCFS and Round Robin (not priority variants)
        unique_arrivals = (algorithm == "FCFS" or algorithm.startswith("Round Robin (Q="))
        
        self.processes = ProcessGenerator.generate_processes(unique_arrivals=unique_arrivals)
        
        # If using Round Robin, also randomize quantum
        if "Round Robin" in algorithm:
            quantum = ProcessGenerator.generate_quantum()
            self.quantum_spinbox.setValue(quantum)
            self.update_round_robin_scheduler()
        
        # Clear any existing solution state
        self.solution_result = None
        self.current_schedule = []
        self.is_locked = False
        
        # Update both table and grid
        self.update_process_table()
        self.update_timeline_grid()
        
        # Clear results display
        if self.results_label:
            self.results_label.setText("")

    def read_process_table(self):
        """Read processes from the table."""
        self.processes = []
        for i in range(self.process_table.rowCount()):
            process_id = self.process_table.item(i, 0).text()
            priority = int(self.process_table.item(i, 1).text())
            arrival = int(self.process_table.item(i, 2).text())
            burst = int(self.process_table.item(i, 3).text())
            self.processes.append(Process(process_id, priority, arrival, burst))

    def check_solution(self):
        """Check the student's solution against the correct solution."""
        self.read_process_table()
        
        # Get the selected algorithm
        algorithm_name = self.algorithm_combo.currentText()
        scheduler = self.schedulers[algorithm_name]
        
        # Calculate correct solution
        self.solution_result = scheduler.schedule(self.processes)
        
        # Get student's schedule
        student_schedule = self.get_student_schedule()
        
        # Compare schedules
        mismatches = []
        min_len = min(len(student_schedule), len(self.solution_result.timeline))
        
        for i in range(min_len):
            if student_schedule[i] != self.solution_result.timeline[i]:
                mismatches.append(i)
        
        # Display results
        if not mismatches:
            result_text = "<b>✓ Correct solution!</b><br><br>"
        else:
            result_text = f"<b>✗ Incorrect.</b> Mismatches at times: {mismatches[:10]}<br><br>"
        
        # Add metrics
        result_text += "<b>Waiting & Turnaround Times:</b><br>"
        total_waiting = 0
        total_turnaround = 0
        
        for process_id, metrics in self.solution_result.process_metrics.items():
            waiting = metrics.waiting
            turnaround = metrics.turnaround
            result_text += f"Process {process_id}: WT={waiting}, TAT={turnaround}<br>"
            total_waiting += waiting
            total_turnaround += turnaround
        
        if len(self.solution_result.process_metrics) > 0:
            avg_waiting = self.solution_result.get_average_waiting_time()
            avg_turnaround = self.solution_result.get_average_turnaround_time()
            result_text += f"<br><b>Average: WT={avg_waiting:.1f}, TAT={avg_turnaround:.1f}</b>"
        
        # Add responsiveness calculations
        result_text += "<br><br><b>Responsiveness (Burst/TAT):</b><br>"
        total_responsiveness = 0
        process_count = 0
        
        for process_id, metrics in self.solution_result.process_metrics.items():
            # Find the process to get its burst time
            process = next((p for p in self.processes if p.id == process_id), None)
            if process and metrics.turnaround > 0:
                responsiveness = process.burst / metrics.turnaround
                result_text += f"Process {process_id}: {responsiveness:.3f}<br>"
                total_responsiveness += responsiveness
                process_count += 1
        
        if process_count > 0:
            avg_responsiveness = total_responsiveness / process_count
            result_text += f"<br><b>Average Responsiveness: {avg_responsiveness:.3f}</b>"
        
        self.results_label.setText(result_text)

    def show_solution(self):
        """Show the correct solution."""
        self.read_process_table()
        
        # Get the selected algorithm
        algorithm_name = self.algorithm_combo.currentText()
        scheduler = self.schedulers[algorithm_name]
        
        # Calculate solution
        self.solution_result = scheduler.schedule(self.processes)
        
        # Fill the grid with the solution
        self.fill_grid_with_schedule(self.solution_result.timeline)
        self.is_locked = True
        
        # Show metrics
        result_text = "<b>Solution displayed and locked.</b><br><br>"
        result_text += "<b>Waiting & Turnaround Times:</b><br>"
        
        for process_id, metrics in self.solution_result.process_metrics.items():
            waiting = metrics.waiting
            turnaround = metrics.turnaround
            result_text += f"Process {process_id}: WT={waiting}, TAT={turnaround}<br>"
        
        if len(self.solution_result.process_metrics) > 0:
            avg_waiting = self.solution_result.get_average_waiting_time()
            avg_turnaround = self.solution_result.get_average_turnaround_time()
            result_text += f"<br><b>Average: WT={avg_waiting:.1f}, TAT={avg_turnaround:.1f}</b>"
        
        # Add responsiveness calculations
        result_text += "<br><br><b>Responsiveness (Burst/TAT):</b><br>"
        total_responsiveness = 0
        process_count = 0
        
        for process_id, metrics in self.solution_result.process_metrics.items():
            # Find the process to get its burst time
            process = next((p for p in self.processes if p.id == process_id), None)
            if process and metrics.turnaround > 0:
                responsiveness = process.burst / metrics.turnaround
                result_text += f"Process {process_id}: {responsiveness:.3f}<br>"
                total_responsiveness += responsiveness
                process_count += 1
        
        if process_count > 0:
            avg_responsiveness = total_responsiveness / process_count
            result_text += f"<br><b>Average Responsiveness: {avg_responsiveness:.3f}</b>"
        
        self.results_label.setText(result_text)

    def reset_grid(self):
        """Reset the grid to its initial state."""
        self.is_locked = False
        self.results_label.setText("")
        
        # Clear RS markers
        self.rs_markers.clear()
        
        for i in range(self.timeline_grid.rowCount()):
            for j in range(1, self.timeline_grid.columnCount()):
                item = self.timeline_grid.item(i, j)
                if item:
                    item.setBackground(Qt.white)
                    item.setText("")
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    item.setForeground(QColor(0, 0, 0))  # Reset text color

    def get_student_schedule(self) -> List[Optional[str]]:
        """Get the student's schedule from the grid."""
        schedule = []
        
        # Grid columns 1-32 represent times 1-32
        for time_col in range(1, 33):
            assigned_process = None
            for row in range(self.timeline_grid.rowCount()):
                item = self.timeline_grid.item(row, time_col)
                if item:
                    # Check if cell is colored (not white) - compare with current scheduling block color
                    item_color = item.background().color()
                    # A cell is considered scheduled if it's not white and has text content
                    is_white = item_color == Qt.white or item_color.name().lower() == "#ffffff"
                    has_content = item.text() and item.text().strip() and item.text() != "RS"
                    
                    if not is_white and has_content:
                        process_id = self.timeline_grid.item(row, 0).text()
                        assigned_process = process_id
                        break
            schedule.append(assigned_process)
        
        return schedule

    def fill_grid_with_schedule(self, schedule: List[Optional[str]]):
        """Fill the grid with a given schedule."""
        # Clear grid first
        for i in range(self.timeline_grid.rowCount()):
            for j in range(1, self.timeline_grid.columnCount()):
                item = self.timeline_grid.item(i, j)
                if item:
                    item.setBackground(Qt.white)
                    item.setText("")
                    item.setForeground(QColor(0, 0, 0))  # Reset text color
        
        # Fill with schedule
        process_to_row = {}
        for i, process in enumerate(self.processes):
            process_to_row[process.id] = i
        
        # Timeline index i corresponds to grid column i+1 (time i+1)
        for time_index, process_id in enumerate(schedule):
            grid_col = time_index + 1  # Convert timeline index to grid column
            if process_id and grid_col < self.timeline_grid.columnCount():
                if process_id in process_to_row:
                    row = process_to_row[process_id]
                    item = self.timeline_grid.item(row, grid_col)
                    if item:
                        item.setBackground(self.scheduling_block_color)
                        item.setText("-")
                        item.setForeground(QColor(0, 0, 0))  # Black text
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
