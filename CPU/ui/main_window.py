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
        self.unified_table: Optional[QTableWidget] = None  # Unified table replaces both process_table and timeline_grid
        self.current_schedule: List[Optional[str]] = []
        self.solution_result: Optional[SchedulingResult] = None
        self.is_locked = False
        self.results_label: Optional[QLabel] = None
        self.results_scroll_area: Optional[QScrollArea] = None
        self.algorithm_name_label: Optional[QLabel] = None
        self.quantum_spinbox: Optional[QSpinBox] = None
        self.rs_markers = {}  # Track RS markers: {(row, col): True}
        self._updating_table = False  # Flag to prevent recursion
        
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
        self.update_unified_table()

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
        
        # Fixed spacing below dropdown (same height as a label would take)
        main_layout.addSpacing(20)
        
        # Unified table (combines process input + timeline grid)
        self.setup_unified_table()
        main_layout.addWidget(self.unified_table, stretch=1)  # Table expands to fill available space
        
        # Add tiny spacing between table and console
        main_layout.addSpacing(8)
        
        # Console/Results section - directly under the table
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
        
        # Add spacing between console and buttons
        main_layout.addSpacing(15)
        
        # Buttons section - centered with spacing from bottom
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        # Add stretch to center buttons horizontally
        buttons_layout.addStretch()
        
        # Button rows container
        buttons_container = QVBoxLayout()
        buttons_container.setSpacing(10)
        
        # Uniform button size - all buttons exactly the same
        btn_width = 130
        btn_height = 40
        btn_style = f"min-width: {btn_width}px; max-width: {btn_width}px; min-height: {btn_height}px; max-height: {btn_height}px;"
        
        # First row of buttons
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(10)
        
        add_btn = QPushButton("Add Process")
        add_btn.clicked.connect(self.add_process)
        add_btn.setFixedWidth(btn_width)
        add_btn.setFixedHeight(btn_height)
        add_btn.setStyleSheet(btn_style)
        
        delete_btn = QPushButton("Delete Process")
        delete_btn.clicked.connect(self.delete_process)
        delete_btn.setFixedWidth(btn_width)
        delete_btn.setFixedHeight(btn_height)
        delete_btn.setStyleSheet(btn_style)
        
        randomize_btn = QPushButton("Randomize")
        randomize_btn.clicked.connect(self.randomize_processes)
        randomize_btn.setFixedWidth(btn_width)
        randomize_btn.setFixedHeight(btn_height)
        randomize_btn.setStyleSheet(btn_style)
        
        row1_layout.addWidget(add_btn)
        row1_layout.addWidget(delete_btn)
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
        reset_btn.clicked.connect(self.reset_grid)
        reset_btn.setFixedWidth(btn_width)
        reset_btn.setFixedHeight(btn_height)
        reset_btn.setStyleSheet(btn_style)
        
        row2_layout.addWidget(check_btn)
        row2_layout.addWidget(show_btn)
        row2_layout.addWidget(reset_btn)
        buttons_container.addLayout(row2_layout)
        
        buttons_layout.addLayout(buttons_container)
        
        # Add stretch to center buttons horizontally
        buttons_layout.addStretch()
        
        main_layout.addLayout(buttons_layout)
        
        # Add spacing at the bottom of the page
        main_layout.addSpacing(25)

    def setup_unified_table(self):
        """Set up the unified table combining process input and timeline grid."""
        # 36 columns: 4 for process input + 32 for timeline
        self.unified_table = QTableWidget(0, 36)
        
        # Set up headers
        headers = ["Process ID", "Priority", "Arrival", "Burst"] + [str(i) for i in range(1, 33)]
        self.unified_table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        self.unified_table.setColumnWidth(0, 70)   # Process ID
        self.unified_table.setColumnWidth(1, 55)   # Priority
        self.unified_table.setColumnWidth(2, 55)   # Arrival
        self.unified_table.setColumnWidth(3, 45)   # Burst
        for i in range(4, 36):
            self.unified_table.setColumnWidth(i, 35)  # Timeline columns
        
        # Connect cell events
        self.unified_table.cellClicked.connect(self.on_cell_clicked)
        self.unified_table.cellEntered.connect(self.on_cell_hover)
        self.unified_table.cellChanged.connect(self.on_cell_changed)
        
        # Enable context menu
        self.unified_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.unified_table.customContextMenuRequested.connect(self.show_context_menu)
        self.unified_table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        
        # Enable mouse tracking for better responsiveness
        self.unified_table.setMouseTracking(True)
        
        # Set row height
        self.unified_table.verticalHeader().setDefaultSectionSize(30)
        self.unified_table.verticalHeader().hide()

    def on_cell_changed(self, row, column):
        """Handle cell value changes in the unified table."""
        if self._updating_table:
            return
        # Only react to changes in editable input columns (1-3: Priority, Arrival, Burst)
        if column < 1 or column > 3:
            return
        # Read and update processes from table
        self.read_process_table()

    def set_scheduling_block_color(self, color):
        """Set the color for scheduling blocks in the timeline grid."""
        old_color = self.scheduling_block_color
        self.scheduling_block_color = QColor(color)
        # Refresh all existing colored blocks with the new color
        self.refresh_colored_blocks(old_color)

    def refresh_colored_blocks(self, old_color):
        """Refresh all colored blocks in the timeline grid with the new color."""
        if not self.unified_table:
            return
            
        # Iterate through all cells in the timeline portion (columns 4+)
        for row in range(self.unified_table.rowCount()):
            for col in range(4, self.unified_table.columnCount()):  # Timeline starts at column 4
                item = self.unified_table.item(row, col)
                if item:
                    item_color = item.background().color()
                    item_text = item.text()
                    
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

    def update_unified_table(self):
        """Update the unified table with current processes."""
        self._updating_table = True
        
        if not self.processes:
            self.unified_table.setRowCount(0)
            self._updating_table = False
            return
        
        # Save current RS markers
        old_rs_markers = self.rs_markers.copy()
        
        self.unified_table.setRowCount(len(self.processes))
        
        for i, process in enumerate(self.processes):
            # Process ID column (read-only)
            id_item = QTableWidgetItem(process.id)
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            id_item.setTextAlignment(Qt.AlignCenter)
            self.unified_table.setItem(i, 0, id_item)
            
            # Priority column (editable)
            priority_item = QTableWidgetItem(str(process.priority))
            priority_item.setTextAlignment(Qt.AlignCenter)
            self.unified_table.setItem(i, 1, priority_item)
            
            # Arrival column (editable)
            arrival_item = QTableWidgetItem(str(process.arrival))
            arrival_item.setTextAlignment(Qt.AlignCenter)
            self.unified_table.setItem(i, 2, arrival_item)
            
            # Burst column (editable)
            burst_item = QTableWidgetItem(str(process.burst))
            burst_item.setTextAlignment(Qt.AlignCenter)
            self.unified_table.setItem(i, 3, burst_item)
            
            # Timeline columns (4-35)
            for j in range(4, 36):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(Qt.white)
                if not self.is_locked:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.unified_table.setItem(i, j, item)
        
        # Restore RS markers
        self.rs_markers = old_rs_markers
        for (row, col) in self.rs_markers:
            if row < self.unified_table.rowCount() and col < self.unified_table.columnCount():
                self.update_cell_display(row, col)
        
        self._updating_table = False

    def on_cell_clicked(self, row: int, col: int):
        """Handle cell click events."""
        # Only handle timeline columns (4+)
        if col < 4 or self.is_locked:
            return
            
        item = self.unified_table.item(row, col)
        if item is None:
            return
            
        # Clear all other cells in this column first
        for r in range(self.unified_table.rowCount()):
            other_item = self.unified_table.item(r, col)
            if other_item and r != row:
                other_item.setBackground(Qt.white)
                other_item.setForeground(QColor(0, 0, 0))
                if (r, col) in self.rs_markers:
                    other_item.setText("RS")
                    other_item.setForeground(QColor(128, 128, 128))
                else:
                    other_item.setText("")
        
        # Toggle current cell
        if item.background().color().name().lower() == self.scheduling_block_color.name().lower():
            item.setBackground(Qt.white)
            item.setForeground(QColor(0, 0, 0))
            if (row, col) in self.rs_markers:
                item.setText("RS")
                item.setForeground(QColor(128, 128, 128))
            else:
                item.setText("")
        else:
            item.setBackground(self.scheduling_block_color)
            item.setForeground(QColor(0, 0, 0))
            if (row, col) in self.rs_markers:
                item.setText("-\nRS")
            else:
                item.setText("-")

    def on_cell_hover(self, row: int, col: int):
        """Handle cell hover events."""
        if col < 4 or self.is_locked:
            return

    def on_cell_double_clicked(self, row: int, col: int):
        """Handle cell double-click events."""
        # Only handle timeline columns (4+)
        if col < 4 or self.is_locked:
            return
            
        item = self.unified_table.item(row, col)
        if item is None:
            return
            
        # Clear all cells in this column first
        for r in range(self.unified_table.rowCount()):
            other_item = self.unified_table.item(r, col)
            if other_item:
                other_item.setBackground(Qt.white)
                other_item.setText("")
        
        # Find the process burst time and fill consecutive cells
        process_id = self.unified_table.item(row, 0).text()
        process = next((p for p in self.processes if p.id == process_id), None)
        
        if process:
            for i in range(process.burst):
                if col + i < self.unified_table.columnCount():
                    cell_item = self.unified_table.item(row, col + i)
                    if cell_item:
                        for r in range(self.unified_table.rowCount()):
                            if r != row:
                                other_item = self.unified_table.item(r, col + i)
                                if other_item:
                                    other_item.setBackground(Qt.white)
                                    other_item.setText("")
                        
                        cell_item.setBackground(self.scheduling_block_color)
                        cell_item.setText("-")

    def show_context_menu(self, position):
        """Show context menu for RS markers."""
        item = self.unified_table.itemAt(position)
        if item is None:
            return
            
        row = item.row()
        col = item.column()
        
        # Only allow RS markers in timeline columns (4+)
        if col < 4:
            return
            
        menu = QMenu(self)
        
        has_rs_marker = (row, col) in self.rs_markers
        
        if has_rs_marker:
            action = menu.addAction("Remove RS Marker")
            action.triggered.connect(lambda: self.remove_rs_marker(row, col))
        else:
            action = menu.addAction("Add RS Marker")
            action.triggered.connect(lambda: self.add_rs_marker(row, col))
            
        menu.exec(self.unified_table.mapToGlobal(position))

    def add_rs_marker(self, row: int, col: int):
        """Add RS marker to a cell."""
        self.remove_rs_markers_in_row(row)
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
        item = self.unified_table.item(row, col)
        if item is None:
            return
            
        has_rs_marker = (row, col) in self.rs_markers
        current_text = item.text()
        
        if has_rs_marker:
            if current_text and current_text != "" and "RS" not in current_text:
                item.setText(f"{current_text}\nRS")
            else:
                item.setText("RS")
            item.setForeground(QColor(128, 128, 128))
        else:
            if current_text and "RS" in current_text:
                new_text = current_text.replace("\nRS", "").replace("RS", "")
                item.setText(new_text)
            item.setForeground(QColor(0, 0, 0))

    def on_algorithm_changed(self):
        """Handle algorithm selection change."""
        algorithm = self.algorithm_combo.currentText()
        
        is_round_robin = "Round Robin" in algorithm
        self.quantum_label.setVisible(is_round_robin)
        self.quantum_spinbox.setVisible(is_round_robin)
        
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
        new_process = Process(next_id, 1, 1, 1)
        self.processes.append(new_process)
        
        self.solution_result = None
        self.current_schedule = []
        self.is_locked = False
        
        self.update_unified_table()
        if self.results_label:
            self.results_label.setText("")

    def delete_process(self):
        """Delete the last process."""
        if self.processes:
            self.processes.pop()
            
            self.solution_result = None
            self.current_schedule = []
            self.is_locked = False
            
            self.update_unified_table()
            if self.results_label:
                self.results_label.setText("")

    def randomize_processes(self):
        """Generate random processes."""
        algorithm = self.algorithm_combo.currentText()
        
        algorithms_needing_unique_arrivals = ["FCFS", "Round Robin (Q="]
        unique_arrivals = (algorithm == "FCFS" or algorithm.startswith("Round Robin (Q="))
        
        self.processes = ProcessGenerator.generate_processes(unique_arrivals=unique_arrivals)
        
        if "Round Robin" in algorithm:
            quantum = ProcessGenerator.generate_quantum()
            self.quantum_spinbox.setValue(quantum)
            self.update_round_robin_scheduler()
        
        self.solution_result = None
        self.current_schedule = []
        self.is_locked = False
        
        self.update_unified_table()
        
        if self.results_label:
            self.results_label.setText("")

    def read_process_table(self):
        """Read processes from the unified table (columns 0-3)."""
        self.processes = []
        for i in range(self.unified_table.rowCount()):
            try:
                process_id = self.unified_table.item(i, 0).text() if self.unified_table.item(i, 0) else chr(ord('A') + i)
                priority = int(self.unified_table.item(i, 1).text()) if self.unified_table.item(i, 1) else 1
                arrival = int(self.unified_table.item(i, 2).text()) if self.unified_table.item(i, 2) else 1
                burst = int(self.unified_table.item(i, 3).text()) if self.unified_table.item(i, 3) else 1
                self.processes.append(Process(process_id, priority, arrival, burst))
            except (ValueError, AttributeError):
                pass

    def check_solution(self):
        """Check the student's solution against the correct solution."""
        self.read_process_table()
        
        algorithm_name = self.algorithm_combo.currentText()
        scheduler = self.schedulers[algorithm_name]
        
        self.solution_result = scheduler.schedule(self.processes)
        
        student_schedule = self.get_student_schedule()
        
        mismatches = []
        min_len = min(len(student_schedule), len(self.solution_result.timeline))
        
        for i in range(min_len):
            if student_schedule[i] != self.solution_result.timeline[i]:
                mismatches.append(i)
        
        if not mismatches:
            result_text = "<b>✓ Correct solution!</b><br><br>"
        else:
            result_text = f"<b>✗ Incorrect.</b> Mismatches at times: {mismatches[:10]}<br><br>"
        
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
        
        result_text += "<br><br><b>Responsiveness (Burst/TAT):</b><br>"
        total_responsiveness = 0
        process_count = 0
        
        for process_id, metrics in self.solution_result.process_metrics.items():
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
        
        algorithm_name = self.algorithm_combo.currentText()
        scheduler = self.schedulers[algorithm_name]
        
        self.solution_result = scheduler.schedule(self.processes)
        
        self.fill_grid_with_schedule(self.solution_result.timeline)
        self.is_locked = True
        
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
        
        result_text += "<br><br><b>Responsiveness (Burst/TAT):</b><br>"
        total_responsiveness = 0
        process_count = 0
        
        for process_id, metrics in self.solution_result.process_metrics.items():
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
        
        self.rs_markers.clear()
        
        # Reset only timeline columns (4+)
        for i in range(self.unified_table.rowCount()):
            for j in range(4, self.unified_table.columnCount()):
                item = self.unified_table.item(i, j)
                if item:
                    item.setBackground(Qt.white)
                    item.setText("")
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    item.setForeground(QColor(0, 0, 0))

    def get_student_schedule(self) -> List[Optional[str]]:
        """Get the student's schedule from the grid."""
        schedule = []
        
        # Timeline columns 4-35 represent times 1-32
        for time_col in range(4, 36):
            assigned_process = None
            for row in range(self.unified_table.rowCount()):
                item = self.unified_table.item(row, time_col)
                if item:
                    item_color = item.background().color()
                    is_white = item_color == Qt.white or item_color.name().lower() == "#ffffff"
                    has_content = item.text() and item.text().strip() and item.text() != "RS"
                    
                    if not is_white and has_content:
                        process_id = self.unified_table.item(row, 0).text()
                        assigned_process = process_id
                        break
            schedule.append(assigned_process)
        
        return schedule

    def fill_grid_with_schedule(self, schedule: List[Optional[str]]):
        """Fill the grid with a given schedule."""
        # Clear timeline portion only (columns 4+)
        for i in range(self.unified_table.rowCount()):
            for j in range(4, self.unified_table.columnCount()):
                item = self.unified_table.item(i, j)
                if item:
                    item.setBackground(Qt.white)
                    item.setText("")
                    item.setForeground(QColor(0, 0, 0))
        
        process_to_row = {}
        for i, process in enumerate(self.processes):
            process_to_row[process.id] = i
        
        # Timeline index i corresponds to grid column i+4 (time i+1)
        for time_index, process_id in enumerate(schedule):
            grid_col = time_index + 4  # Convert timeline index to grid column
            if process_id and grid_col < self.unified_table.columnCount():
                if process_id in process_to_row:
                    row = process_to_row[process_id]
                    item = self.unified_table.item(row, grid_col)
                    if item:
                        item.setBackground(self.scheduling_block_color)
                        item.setText("-")
                        item.setForeground(QColor(0, 0, 0))
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
