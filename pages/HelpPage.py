"""
Help Page with CPU Scheduling and Page Replacement Algorithm Tutorials
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                              QStackedWidget, QScrollArea, QGroupBox, QHBoxLayout,
                              QTableWidget, QTableWidgetItem, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QColor
from PySide6.QtCore import QSize


class HelpPage(QWidget):
    """Help page with tutorials for CPU Scheduling and Page Replacement Algorithms"""
    
    def __init__(self):
        super().__init__()
        self.current_theme = {}
        self.example_pages = {}  # Store example pages by algorithm name
        self.example_page_widgets = {}  # Store actual QWidget references for theme updates
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the help page UI"""
        # Main layout with stack for switching between menu and tutorials
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Stacked widget to switch between main menu and tutorial pages
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)
        
        # Create main menu page (index 0)
        self.menu_page = self.create_menu_page()
        self.stack.addWidget(self.menu_page)
        
        # Create CPU scheduling tutorial page (index 1)
        self.cpu_tutorial_page = self.create_cpu_tutorial_page()
        self.stack.addWidget(self.cpu_tutorial_page)
        
        # Create PRA tutorial page (index 2)
        self.pra_tutorial_page = self.create_pra_tutorial_page()
        self.stack.addWidget(self.pra_tutorial_page)
        
        # Example pages will be added dynamically starting from index 3
        
        # Start with menu page
        self.stack.setCurrentIndex(0)
    
    def create_menu_page(self):
        """Create the main menu page with tutorial options"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        
        # Title
        self.menu_title = QLabel("Help & Tutorials")
        self.menu_title.setObjectName("helpMenuTitle")
        self.menu_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.menu_title)
        
        # Subtitle
        self.menu_subtitle = QLabel("Select a topic to learn more")
        self.menu_subtitle.setObjectName("helpMenuSubtitle")
        self.menu_subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.menu_subtitle)
        
        layout.addSpacing(30)
        
        # Container for menu buttons
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(20)
        
        # CPU Scheduling Tutorial Button
        self.cpu_btn = QPushButton("  CPU Scheduling Tutorials")
        self.cpu_btn.setObjectName("cpuTutorialBtn")
        self.cpu_btn.setIcon(QIcon("Assets/icons/CPU_Tutorial.png"))
        self.cpu_btn.setIconSize(QSize(32, 32))
        self.cpu_btn.setCursor(Qt.PointingHandCursor)
        self.cpu_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        button_layout.addWidget(self.cpu_btn)
        
        # PRA Tutorial Button
        self.pra_btn = QPushButton("  Page Replacement Tutorials")
        self.pra_btn.setObjectName("praTutorialBtn")
        self.pra_btn.setIcon(QIcon("Assets/icons/PRA_Tutorial.png"))
        self.pra_btn.setIconSize(QSize(32, 32))
        self.pra_btn.setCursor(Qt.PointingHandCursor)
        self.pra_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        button_layout.addWidget(self.pra_btn)
        
        layout.addWidget(button_container)
        layout.addStretch()
        
        return page
    
    def create_cpu_tutorial_page(self):
        """Create the CPU scheduling tutorial page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Back button
        self.cpu_back_btn = QPushButton("← Back to Menu")
        self.cpu_back_btn.setObjectName("backBtn")
        self.cpu_back_btn.setMaximumWidth(150)
        self.cpu_back_btn.setCursor(Qt.PointingHandCursor)
        self.cpu_back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(self.cpu_back_btn)
        
        # Scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("tutorialScrollArea")
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Title
        self.cpu_title = QLabel("CPU Scheduling Algorithms")
        self.cpu_title.setObjectName("tutorialTitle")
        content_layout.addWidget(self.cpu_title)
        
        # Tutorial content
        tutorials = [
            ("First Come First Served (FCFS)", self.get_fcfs_tutorial()),
            ("Shortest Job First (SJF)", self.get_sjf_tutorial()),
            ("Shortest Remaining Time (SRT)", self.get_srt_tutorial()),
            ("Round Robin (RR)", self.get_rr_tutorial()),
            ("Priority Scheduling", self.get_priority_tutorial()),
        ]
        
        self.cpu_sections = []
        for algo_name, tutorial_text in tutorials:
            # Algorithm section
            section = QGroupBox(algo_name)
            section.setObjectName("tutorialSection")
            
            section_layout = QVBoxLayout(section)
            
            tutorial_label = QLabel(tutorial_text)
            tutorial_label.setObjectName("tutorialContent")
            tutorial_label.setWordWrap(True)
            tutorial_label.setTextFormat(Qt.RichText)
            section_layout.addWidget(tutorial_label)
            
            # Example button
            example_btn = QPushButton("📝 View Example")
            example_btn.setObjectName("exampleBtn")
            example_btn.setCursor(Qt.PointingHandCursor)
            example_btn.setMaximumWidth(200)
            example_btn.clicked.connect(lambda checked, name=algo_name: self.show_example_page(name, "CPU"))
            section_layout.addWidget(example_btn)
            
            content_layout.addWidget(section)
            self.cpu_sections.append(section)
        
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        
        return page
    
    def create_pra_tutorial_page(self):
        """Create the PRA tutorial page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Back button
        self.pra_back_btn = QPushButton("← Back to Menu")
        self.pra_back_btn.setObjectName("backBtn")
        self.pra_back_btn.setMaximumWidth(150)
        self.pra_back_btn.setCursor(Qt.PointingHandCursor)
        self.pra_back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(self.pra_back_btn)
        
        # Scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("tutorialScrollArea")
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Title
        self.pra_title = QLabel("Page Replacement Algorithms")
        self.pra_title.setObjectName("tutorialTitle")
        content_layout.addWidget(self.pra_title)
        
        # Tutorial content
        tutorials = [
            ("First In First Out (FIFO)", self.get_fifo_tutorial()),
            ("Least Recently Used (LRU)", self.get_lru_tutorial()),
            ("Optimal Page Replacement", self.get_optimal_tutorial()),
            ("Second Chance (Clock)", self.get_second_chance_tutorial()),
        ]
        
        self.pra_sections = []
        for algo_name, tutorial_text in tutorials:
            # Algorithm section
            section = QGroupBox(algo_name)
            section.setObjectName("tutorialSection")
            
            section_layout = QVBoxLayout(section)
            
            tutorial_label = QLabel(tutorial_text)
            tutorial_label.setObjectName("tutorialContent")
            tutorial_label.setWordWrap(True)
            tutorial_label.setTextFormat(Qt.RichText)
            section_layout.addWidget(tutorial_label)
            
            # Example button
            example_btn = QPushButton("📝 View Example")
            example_btn.setObjectName("exampleBtn")
            example_btn.setCursor(Qt.PointingHandCursor)
            example_btn.setMaximumWidth(200)
            example_btn.clicked.connect(lambda checked, name=algo_name: self.show_example_page(name, "PRA"))
            section_layout.addWidget(example_btn)
            
            content_layout.addWidget(section)
            self.pra_sections.append(section)
        
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        
        return page
    
    def apply_theme(self, theme: dict):
        """Apply theme colors to the help page"""
        self.current_theme = theme
        
        # Apply to the entire help page
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {theme['main_bg']};
                color: {theme['text_primary']};
            }}
            
            /* Menu page styles */
            QLabel#helpMenuTitle {{
                font-size: 32px;
                font-weight: bold;
                color: {theme['text_primary']};
            }}
            
            QLabel#helpMenuSubtitle {{
                font-size: 16px;
                color: {theme['text_secondary']};
            }}
            
            QPushButton#cpuTutorialBtn {{
                background-color: {theme.get('button_bg', '#7289da')};
                border: none;
                padding: 20px 40px;
                border-radius: 8px;
                color: {theme.get('button_text', theme['text_primary'])};
                font-size: 18px;
                font-weight: bold;
                text-align: left;
            }}
            
            QPushButton#cpuTutorialBtn:hover {{
                background-color: {theme.get('button_hover', '#677bc4')};
            }}
            
            QPushButton#praTutorialBtn {{
                background-color: {theme.get('sidebar_accent', '#43b581')};
                border: none;
                padding: 20px 40px;
                border-radius: 8px;
                color: {theme.get('button_text', theme['text_primary'])};
                font-size: 18px;
                font-weight: bold;
                text-align: left;
            }}
            
            QPushButton#praTutorialBtn:hover {{
                background-color: {theme.get('input_border', '#3ca374')};
            }}
            
            /* Tutorial page styles */
            QPushButton#backBtn {{
                background-color: {theme.get('input_bg', '#40444b')};
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                color: {theme['text_primary']};
                font-size: 14px;
                text-align: left;
            }}
            
            QPushButton#backBtn:hover {{
                background-color: {theme.get('sidebar_hover', '#4a4f56')};
            }}
            
            QLabel#tutorialTitle {{
                font-size: 28px;
                font-weight: bold;
                color: {theme['text_primary']};
                margin-bottom: 10px;
            }}
            
            QGroupBox#tutorialSection {{
                font-size: 18px;
                font-weight: bold;
                color: {theme.get('button_bg', '#7289da')};
                border: 2px solid {theme.get('input_border', '#40444b')};
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: {theme.get('header_bg', '#2c2f33')};
            }}
            
            QGroupBox#tutorialSection::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px 0 5px;
            }}
            
            QLabel#tutorialContent {{
                color: {theme['text_primary']};
                font-size: 14px;
                line-height: 1.6;
            }}
            
            QScrollArea#tutorialScrollArea {{
                border: none;
                background-color: transparent;
            }}
            
            /* Example button styles */
            QPushButton#exampleBtn {{
                background-color: {theme.get('sidebar_accent', '#43b581')};
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                color: {theme.get('button_text', theme['text_primary'])};
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }}
            
            QPushButton#exampleBtn:hover {{
                background-color: {theme.get('input_border', '#3ca374')};
            }}
            
            /* Example page styles */
            QLabel#exampleTitle {{
                font-size: 24px;
                font-weight: bold;
                color: {theme['text_primary']};
                margin-bottom: 15px;
            }}
            
            QLabel#stepTitle {{
                font-size: 16px;
                font-weight: bold;
                color: {theme.get('button_bg', '#7289da')};
                margin-top: 10px;
                margin-bottom: 5px;
            }}
            
            QLabel#stepContent {{
                color: {theme['text_primary']};
                font-size: 14px;
                line-height: 1.5;
            }}
            
            /* Interactive example page styles */
            QFrame#vizContainer {{
                background-color: {theme.get('main_bg', '#2c2f33')};
                border: 2px solid {theme.get('input_border', '#40444b')};
                border-radius: 8px;
                padding: 10px;
            }}
            
            QTableWidget#ganttTable {{
                background-color: {theme.get('table_bg', '#40444b')};
                border: 1px solid {theme.get('table_grid', '#666')};
                gridline-color: {theme.get('table_grid', '#666')};
                color: {theme['text_primary']};
            }}
            
            QTableWidget#ganttTable QHeaderView::section {{
                background-color: {theme.get('header_bg', '#2c2f33')};
                color: {theme['text_primary']};
                padding: 5px;
                border: 1px solid {theme.get('table_grid', '#666')};
                font-weight: bold;
            }}
            
            QLabel#stepExplanation {{
                background-color: {theme.get('input_bg', '#40444b')};
                border: 2px solid {theme.get('button_bg', '#7289da')};
                border-radius: 5px;
                padding: 15px;
                color: {theme['text_primary']};
                font-size: 14px;
                line-height: 1.6;
            }}
            
            QPushButton#navBtn {{
                background-color: {theme.get('button_bg', '#7289da')};
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                color: {theme.get('button_text', theme['text_primary'])};
                font-size: 14px;
                font-weight: bold;
            }}
            
            QPushButton#navBtn:hover {{
                background-color: {theme.get('button_hover', '#677bc4')};
            }}
            
            QPushButton#navBtn:disabled {{
                background-color: {theme.get('input_bg', '#40444b')};
                color: {theme.get('text_secondary', '#666')};
            }}
            
            QPushButton#resetBtn {{
                background-color: {theme.get('sidebar_accent', '#43b581')};
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                color: {theme.get('button_text', theme['text_primary'])};
                font-size: 14px;
                font-weight: bold;
            }}
            
            QPushButton#resetBtn:hover {{
                background-color: {theme.get('input_border', '#3ca374')};
            }}
            
            QLabel#stepCounter {{
                color: {theme['text_primary']};
                font-size: 16px;
                font-weight: bold;
                padding: 0 20px;
            }}
            
            QLabel#staticStepsHeader {{
                color: {theme.get('button_bg', '#7289da')};
                font-size: 20px;
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 10px;
            }}
        """)
        
        # Apply theme to all already-created example pages
        for page_key, example_page_widget in self.example_page_widgets.items():
            example_page_widget.setStyleSheet(self.styleSheet())
    
    def setup_gantt_table(self, table, algo_name, category):
        """Setup the Gantt chart table like the CPU scheduling visualization"""
        if category == "CPU":
            # Create table with processes as rows and columns for: Process ID, Priority, Arrival, Burst, + Time units
            num_processes = 4
            num_time_units = self.get_timeline_length(algo_name, category)
            
            # Columns: Process ID, Priority, Arrival, Burst Time, then time units (1-30)
            total_cols = 4 + num_time_units
            table.setRowCount(num_processes)
            table.setColumnCount(total_cols)
            
            # Set column headers
            headers = ["Process ID", "Priority", "Arrival", "Burst time"] + [str(i+1) for i in range(num_time_units)]
            table.setHorizontalHeaderLabels(headers)
            
            # Process data (matching the image)
            processes_data = [
                ["A", "4", "11", "8"],
                ["B", "1", "13", "9"],
                ["C", "2", "6", "9"],
                ["D", "3", "1", "6"]
            ]
            
            # Fill the table
            for row, process_data in enumerate(processes_data):
                # First 4 columns: Process info
                for col, value in enumerate(process_data):
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    # Color the process ID column header slightly different
                    if col == 0:
                        item.setBackground(QColor("#3a3f4b"))
                    table.setItem(row, col, item)
                
                # Remaining columns: Timeline cells (initially empty/gray)
                for col in range(4, total_cols):
                    item = QTableWidgetItem("")
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    item.setBackground(QColor("#2a2a2a"))
                    table.setItem(row, col, item)
            
            # Set column widths
            table.setColumnWidth(0, 80)  # Process ID
            table.setColumnWidth(1, 70)  # Priority
            table.setColumnWidth(2, 70)  # Arrival
            table.setColumnWidth(3, 90)  # Burst time
            for col in range(4, total_cols):
                table.setColumnWidth(col, 35)  # Time unit columns
            
            # Set table properties - use fixed height to prevent shrinking
            table.setFixedHeight(220)
            table.setShowGrid(True)
            table.verticalHeader().setVisible(False)
            
            # Disable automatic resizing
            table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
            table.horizontalHeader().setStretchLastSection(False)
            
        elif category == "PRA":
            # Page replacement visualization
            num_frames = 3
            num_references = 10
            
            table.setRowCount(num_frames + 1)
            table.setColumnCount(num_references)
            
            table.setVerticalHeaderLabels(["Ref"] + [f"Frame {i+1}" for i in range(num_frames)])
            
            # Fill with empty cells
            for row in range(num_frames + 1):
                for col in range(num_references):
                    cell_item = QTableWidgetItem("")
                    cell_item.setTextAlignment(Qt.AlignCenter)
                    cell_item.setFlags(cell_item.flags() & ~Qt.ItemIsEditable)
                    table.setItem(row, col, cell_item)
            
            for col in range(num_references):
                table.setColumnWidth(col, 50)
            
            table.setMinimumHeight(200)
            table.setMaximumHeight(250)
            table.setShowGrid(True)
            table.horizontalHeader().setVisible(False)
    
    def get_timeline_length(self, algo_name, category):
        """Get the number of time units for the timeline"""
        if category == "CPU":
            # Extended to 30 to show all processes (D ends at 7, C at 15, A at 19, B at 22)
            return 30
        elif category == "PRA":
            return 10  # For page reference sequence
        return 20
    
    def next_step(self, page):
        """Move to the next step in the simulation"""
        if page.current_step < page.total_steps:
            page.current_step += 1
            self.update_simulation(page)
    
    def prev_step(self, page):
        """Move to the previous step"""
        if page.current_step > 0:
            page.current_step -= 1
            self.update_simulation(page)
    
    def reset_simulation(self, page):
        """Reset the simulation to the beginning"""
        page.current_step = 0
        self.update_simulation(page)
    
    def update_simulation(self, page):
        """Update the visualization based on current step"""
        step_num = page.current_step
        total_steps = page.total_steps
        
        # Update step counter
        page.step_counter.setText(f"Step {step_num} / {total_steps}")
        
        # Update navigation buttons
        page.prev_btn.setEnabled(step_num > 0)
        page.next_btn.setEnabled(step_num < total_steps)
        
        # Update step explanation
        if step_num == 0:
            page.step_explanation.setText("Click 'Next Step' to begin the simulation")
            # Clear Gantt table
            self.clear_gantt_table(page.gantt_table, page.category)
        else:
            # For FCFS, use specific step explanations for each process execution
            if page.category == "CPU" and "First Come First Served" in page.algo_name:
                # Map step numbers to the correct example_steps indices
                # Step 1 (D) -> example_steps[1], Step 2 (C) -> example_steps[2], etc.
                step_index = step_num  # Direct mapping: step 1->index 1, step 2->index 2, etc.
                if step_index < len(page.example_steps):
                    step_title, step_text = page.example_steps[step_index]
                    page.step_explanation.setText(f"<b>{step_title}</b><br><br>{step_text}")
            else:
                # For other algorithms, use the default mapping
                step_title, step_text = page.example_steps[step_num - 1]
                page.step_explanation.setText(f"<b>{step_title}</b><br><br>{step_text}")
            
            # Update Gantt table visualization
            self.update_gantt_table(page, step_num)
    
    def clear_gantt_table(self, table, category):
        """Clear all colored cells in the Gantt table (only timeline columns)"""
        if category == "CPU":
            # Clear only the timeline columns (column 4 onwards)
            for row in range(table.rowCount()):
                for col in range(4, table.columnCount()):
                    item = table.item(row, col)
                    if item:
                        item.setText("")
                        item.setBackground(QColor("#2a2a2a"))
        elif category == "PRA":
            for row in range(table.rowCount()):
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    if item:
                        item.setText("")
                        item.setBackground(QColor("#2a2a2a"))
        
        # Force table repaint
        table.viewport().update()
    
    def update_gantt_table(self, page, step_num):
        """Update the Gantt table visualization for the current step"""
        algo_name = page.algo_name
        category = page.category
        table = page.gantt_table
        
        if category != "CPU":
            return
        
        # Process data (same for all CPU algorithms)
        processes = [
            {"id": "A", "priority": 4, "arrival": 11, "burst": 8, "row": 0},
            {"id": "B", "priority": 1, "arrival": 13, "burst": 9, "row": 1},
            {"id": "C", "priority": 2, "arrival": 6, "burst": 9, "row": 2},
            {"id": "D", "priority": 3, "arrival": 1, "burst": 6, "row": 3},
        ]
        
        # Color mapping for each process
        color_map = {
            "A": "#bd93f9",  # Purple
            "B": "#50fa7b",  # Green
            "C": "#ff79c6",  # Pink
            "D": "#8be9fd",  # Cyan
        }
        
        # Clear the table first to reset all colors
        self.clear_gantt_table(table, category)
        
        # Generate timeline based on algorithm
        timeline = None
        execution_order = []
        
        if "First Come First Served (FCFS)" == algo_name:
            timeline, execution_order = self._simulate_fcfs(processes)
        elif "FCFS with Priority" in algo_name:
            timeline, execution_order = self._simulate_fcfs_priority(processes)
        elif "Shortest Job First" in algo_name:
            timeline, execution_order = self._simulate_sjf(processes)
        elif "Shortest Remaining Time" in algo_name:
            timeline, execution_order = self._simulate_srt(processes)
        elif "Round Robin" in algo_name:
            timeline, execution_order = self._simulate_rr(processes, quantum=2)
        
        if not execution_order:
            return
        
        # Special handling for FCFS Priority - show cumulative with specific segments per step
        if "FCFS with Priority" in algo_name:
            # FCFS Priority step mapping (cumulative) - Higher number = Higher priority
            # Priority: A(4) > D(3) > C(2) > B(1)
            # Execution: D(1-7) → C starts(7-11) → A preempts(11-19) → C resumes(19-24) → B(24-33)
            # Step 1: Intro (nothing shown)
            # Step 2: D executes (1-7)
            # Step 3: C starts, D + C (1-7, 7-11)
            # Step 4: A preempts C, D + C + A (1-7, 7-11, 11-19)
            # Step 5: C resumes and completes, D + C complete + A (1-7, 7-11, 11-19, 19-24)
            # Step 6: B executes, all processes (1-7, 7-11, 11-19, 19-24, 24-33)
            # Step 7: Final results (same as step 6)
            
            if step_num == 0 or step_num == 1:
                pass  # Nothing shown for intro
            elif step_num >= 2:
                # Always show D (1-7)
                self._fill_time_range(table, color_map, 3, 1, 7, "#8be9fd")  # D is cyan
                
                if step_num >= 3:
                    # Add C first segment (7-11)
                    self._fill_time_range(table, color_map, 2, 7, 11, "#ff79c6")  # C is pink
                
                if step_num >= 4:
                    # Add A segment (11-19)
                    self._fill_time_range(table, color_map, 0, 11, 19, "#bd93f9")  # A is purple
                
                if step_num >= 5:
                    # Add C resume segment (19-24)
                    self._fill_time_range(table, color_map, 2, 19, 24, "#ff79c6")  # C is pink
                
                if step_num >= 6:
                    # Add B segment (24-33)
                    self._fill_time_range(table, color_map, 1, 24, 33, "#50fa7b")  # B is green
        
        # Special handling for SRT - show cumulative with specific segments per step
        elif "Shortest Remaining Time" in algo_name:
            # SRT step mapping (cumulative):
            # Step 1: Intro (nothing shown)
            # Step 2: D (1-7)
            # Step 3: D + C first part (1-7, 7-11)
            # Step 4: D + C complete (1-7, 7-16)
            # Step 5: D + C + A (1-7, 7-16, 16-24)
            # Step 6: D + C + A + B (1-7, 7-16, 16-24, 24-33)
            # Step 7: Final - show all (same as step 6)
            
            if step_num == 0 or step_num == 1:
                pass  # Nothing shown for intro
            elif step_num >= 2:
                # Always show D (1-7)
                self._fill_time_range(table, color_map, 3, 1, 7, "#8be9fd")  # D is cyan
                
                if step_num >= 3:
                    # Add C first part (7-11)
                    self._fill_time_range(table, color_map, 2, 7, 11, "#ff79c6")  # C is pink
                
                if step_num >= 4:
                    # Add C second part (11-16)
                    self._fill_time_range(table, color_map, 2, 11, 16, "#ff79c6")  # C is pink
                
                if step_num >= 5:
                    # Add A (16-24)
                    self._fill_time_range(table, color_map, 0, 16, 24, "#bd93f9")  # A is purple
                
                if step_num >= 6:
                    # Add B (24-33)
                    self._fill_time_range(table, color_map, 1, 24, 33, "#50fa7b")  # B is green
        else:
            # Original cumulative approach for FCFS, SJF, RR
            # Determine step offset based on algorithm
            # FCFS: Step 1 shows process D (no intro step)
            # SJF/RR: Step 1 is intro, Step 2 shows first process
            step_offset = 1
            if "Shortest Job First" in algo_name or "Round Robin" in algo_name:
                step_offset = 2
            
            # Fill the Gantt chart based on the current step
            for i, exec_info in enumerate(execution_order):
                if step_num >= i + step_offset:  # Show this process if we've reached its step
                    row = exec_info["row"]
                    start = exec_info["start"]
                    end = exec_info["end"]
                    process_id = exec_info["id"]
                    color = QColor(color_map[process_id])  # Get color from map using process ID
                    
                    # Fill cells for this process's execution time
                    # Column 4 = time 1, column 5 = time 2, etc.
                    for time_unit in range(start, end):
                        col_index = 3 + time_unit  # Column 4 represents time 1, so offset is 3
                        if col_index < table.columnCount():
                            item = table.item(row, col_index)
                            if item:
                                item.setBackground(color)
                                item.setText("")  # Use colors only, no letters
        
        # Force table to update/repaint
        table.viewport().update()
        table.repaint()
    
    def _fill_time_range(self, table, color_map, row, start_time, end_time, color_hex):
        """Helper function to fill a specific time range for a process with color"""
        color = QColor(color_hex)
        for time_unit in range(start_time, end_time):
            col_index = 3 + time_unit  # Column 4 represents time 1, so offset is 3
            if col_index < table.columnCount():
                item = table.item(row, col_index)
                if item:
                    item.setBackground(color)
                    item.setText("")
    
    def _simulate_fcfs(self, processes):
        """Simulate FCFS algorithm and return timeline and execution order"""
        # Sort processes by arrival time
        sorted_processes = sorted(processes, key=lambda p: (p["arrival"], p["id"]))
        
        current_time = 0
        execution_order = []
        
        for process in sorted_processes:
            arrival = process["arrival"]
            burst = process["burst"]
            
            # Wait for process to arrive if needed
            if current_time < arrival:
                current_time = arrival
            
            start_time = current_time
            end_time = current_time + burst
            
            execution_order.append({
                "id": process["id"],
                "row": process["row"],
                "start": start_time,
                "end": end_time,
                "color": process["id"]
            })
            
            current_time = end_time
        
        return None, execution_order
    
    def _simulate_sjf(self, processes):
        """Simulate SJF algorithm and return timeline and execution order"""
        # Create working copies
        remaining = [p.copy() for p in processes]
        remaining.sort(key=lambda p: (p["arrival"], p["id"]))
        
        ready_queue = []
        current_time = 1
        execution_order = []
        
        while current_time <= 32:
            # Add newly arrived processes to ready queue
            while remaining and remaining[0]["arrival"] <= current_time:
                ready_queue.append(remaining.pop(0))
            
            # Select process with shortest burst time
            if ready_queue:
                ready_queue.sort(key=lambda p: (p["burst"], p["arrival"], p["id"]))
                current_process = ready_queue.pop(0)
                
                start_time = current_time
                end_time = current_time + current_process["burst"]
                
                execution_order.append({
                    "id": current_process["id"],
                    "row": current_process["row"],
                    "start": start_time,
                    "end": end_time,
                    "color": current_process["id"]
                })
                
                current_time = end_time
            else:
                current_time += 1
            
            if not remaining and not ready_queue:
                break
        
        return None, execution_order
    
    def _simulate_srt(self, processes):
        """Simulate SRT algorithm and return timeline and execution segments"""
        # Create working copies with remaining burst time
        remaining = [p.copy() for p in processes]
        for p in remaining:
            p["remaining"] = p["burst"]
        remaining.sort(key=lambda p: (p["arrival"], p["id"]))
        
        ready_queue = []
        current_time = 1
        execution_segments = []
        current_process = None
        segment_start = None
        
        while current_time <= 32:
            # Add newly arrived processes
            while remaining and remaining[0]["arrival"] <= current_time:
                new_p = remaining.pop(0)
                ready_queue.append(new_p)
                
                # Check for preemption
                if current_process and new_p["remaining"] < current_process["remaining"]:
                    # Save current segment
                    if segment_start is not None:
                        execution_segments.append({
                            "id": current_process["id"],
                            "row": current_process["row"],
                            "start": segment_start,
                            "end": current_time,
                            "color": current_process["id"]
                        })
                    ready_queue.append(current_process)
                    current_process = None
                    segment_start = None
            
            # Select process with shortest remaining time
            if current_process is None and ready_queue:
                ready_queue.sort(key=lambda p: (p["remaining"], p["arrival"], p["id"]))
                current_process = ready_queue.pop(0)
                segment_start = current_time
            
            # Execute current process
            if current_process:
                current_process["remaining"] -= 1
                current_time += 1
                
                # Check if process finished or we need to save segment
                if current_process["remaining"] == 0:
                    execution_segments.append({
                        "id": current_process["id"],
                        "row": current_process["row"],
                        "start": segment_start,
                        "end": current_time,
                        "color": current_process["id"]
                    })
                    current_process = None
                    segment_start = None
            else:
                current_time += 1
            
            if not remaining and not ready_queue and current_process is None:
                break
        
        return None, execution_segments
    
    def _simulate_rr(self, processes, quantum=2):
        """Simulate Round Robin algorithm and return timeline and execution segments"""
        # Create working copies with ready state tracking
        remaining = [p.copy() for p in processes]
        for p in remaining:
            p["remaining"] = p["burst"]
            p["ready_state"] = p["arrival"]
        remaining.sort(key=lambda p: (p["arrival"], p["id"]))
        
        ready_queue = []
        current_time = 1
        execution_segments = []
        
        while current_time <= 32:
            # Add newly arrived processes
            while remaining and remaining[0]["arrival"] <= current_time:
                ready_queue.append(remaining.pop(0))
            
            # Pick process with earliest ready state
            if ready_queue:
                ready_queue.sort(key=lambda p: (p["ready_state"], -p["arrival"]))
                current_process = ready_queue.pop(0)
                
                # Execute for quantum
                start_time = current_time
                quantum_used = 0
                
                while quantum_used < quantum and current_process["remaining"] > 0 and current_time <= 32:
                    current_process["remaining"] -= 1
                    quantum_used += 1
                    current_time += 1
                
                execution_segments.append({
                    "id": current_process["id"],
                    "row": current_process["row"],
                    "start": start_time,
                    "end": current_time,
                    "color": current_process["id"]
                })
                
                # Re-add to queue if not finished
                if current_process["remaining"] > 0:
                    current_process["ready_state"] = current_time
                    ready_queue.append(current_process)
            else:
                current_time += 1
            
            if not remaining and not ready_queue:
                break
        
        return None, execution_segments
    
    def _simulate_fcfs_priority(self, processes):
        """Simulate FCFS Priority (preemptive) algorithm and return execution segments
        Higher priority number = higher priority (A=4 is highest, B=1 is lowest)
        """
        # Create working copies with remaining burst time
        remaining = [p.copy() for p in processes]
        for p in remaining:
            p["remaining"] = p["burst"]
        remaining.sort(key=lambda p: (p["arrival"], p["id"]))
        
        ready_queue = []
        current_time = 1
        execution_segments = []
        current_process = None
        segment_start = None
        
        while current_time <= 35:  # Extended to 35 to complete all processes
            # Add newly arrived processes
            while remaining and remaining[0]["arrival"] <= current_time:
                new_p = remaining.pop(0)
                ready_queue.append(new_p)
                
                # Check for preemption: if new process has higher priority (higher number)
                if current_process and new_p["priority"] > current_process["priority"]:
                    # Save current segment
                    if segment_start is not None:
                        execution_segments.append({
                            "id": current_process["id"],
                            "row": current_process["row"],
                            "start": segment_start,
                            "end": current_time,
                            "color": current_process["id"]
                        })
                    ready_queue.append(current_process)
                    current_process = None
                    segment_start = None
            
            # Select process with highest priority (highest number)
            if current_process is None and ready_queue:
                ready_queue.sort(key=lambda p: (-p["priority"], p["arrival"], p["id"]))
                current_process = ready_queue.pop(0)
                segment_start = current_time
            
            # Execute current process
            if current_process:
                current_process["remaining"] -= 1
                current_time += 1
                
                # Check if process finished
                if current_process["remaining"] == 0:
                    execution_segments.append({
                        "id": current_process["id"],
                        "row": current_process["row"],
                        "start": segment_start,
                        "end": current_time,
                        "color": current_process["id"]
                    })
                    current_process = None
                    segment_start = None
            else:
                current_time += 1
            
            if not remaining and not ready_queue and current_process is None:
                break
        
        return None, execution_segments
    
    def get_example_steps(self, algo_name, category):
        """Get the step-by-step solution for an algorithm
        Returns a list of tuples: (step_title, step_content)
        """
        # Renamed from get_example_content to get_example_steps
        return self.get_example_content(algo_name, category)
    
    def show_example_page(self, algo_name, category):
        """Show the example page for a specific algorithm"""
        # Map "Priority Scheduling" tutorial to "FCFS with Priority" example
        if algo_name == "Priority Scheduling":
            algo_name = "FCFS with Priority"
        
        page_key = f"{category}_{algo_name}"
        
        # Create example page if it doesn't exist
        if page_key not in self.example_pages:
            example_page = self.create_example_page(algo_name, category)
            self.example_pages[page_key] = self.stack.count()
            self.example_page_widgets[page_key] = example_page  # Store widget reference
            self.stack.addWidget(example_page)
        
        # Navigate to the example page
        self.stack.setCurrentIndex(self.example_pages[page_key])
    
    def create_example_page(self, algo_name, category):
        """Create an interactive example page for a specific algorithm"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Back button
        back_btn = QPushButton("← Back to Tutorials")
        back_btn.setObjectName("backBtn")
        back_btn.setMaximumWidth(200)
        back_btn.setCursor(Qt.PointingHandCursor)
        # Go back to CPU tutorial (index 1) or PRA tutorial (index 2)
        back_index = 1 if category == "CPU" else 2
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(back_index))
        layout.addWidget(back_btn)
        
        # Title
        title = QLabel(f"{algo_name} - Interactive Example")
        title.setObjectName("exampleTitle")
        layout.addWidget(title)
        
        # Fixed visualization area (Gantt chart table)
        viz_container = QFrame()
        viz_container.setObjectName("vizContainer")
        viz_layout = QVBoxLayout(viz_container)
        viz_layout.setContentsMargins(15, 15, 15, 15)
        
        # Add quantum label for Round Robin
        if "Round Robin" in algo_name:
            quantum_label = QLabel("<b>Time Quantum (Q) = 2</b>")
            quantum_label.setObjectName("quantumLabel")
            quantum_label.setAlignment(Qt.AlignCenter)
            quantum_label.setStyleSheet("font-size: 14px; padding: 5px; color: #43b581;")
            viz_layout.addWidget(quantum_label)
        
        # Create Gantt chart table (like the CPU scheduling visualization)
        gantt_table = QTableWidget()
        gantt_table.setObjectName("ganttTable")
        self.setup_gantt_table(gantt_table, algo_name, category)
        viz_layout.addWidget(gantt_table)
        
        layout.addWidget(viz_container)
        
        # Current step explanation
        step_explanation = QLabel("Click 'Next Step' to begin the simulation")
        step_explanation.setObjectName("stepExplanation")
        step_explanation.setWordWrap(True)
        step_explanation.setMinimumHeight(60)
        layout.addWidget(step_explanation)
        
        # Navigation buttons
        nav_container = QWidget()
        nav_layout = QHBoxLayout(nav_container)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        
        prev_btn = QPushButton("← Previous Step")
        prev_btn.setObjectName("navBtn")
        prev_btn.setCursor(Qt.PointingHandCursor)
        prev_btn.setEnabled(False)
        
        step_counter = QLabel("Step 0 / 0")
        step_counter.setObjectName("stepCounter")
        step_counter.setAlignment(Qt.AlignCenter)
        
        next_btn = QPushButton("Next Step →")
        next_btn.setObjectName("navBtn")
        next_btn.setCursor(Qt.PointingHandCursor)
        
        reset_btn = QPushButton("🔄 Reset")
        reset_btn.setObjectName("resetBtn")
        reset_btn.setCursor(Qt.PointingHandCursor)
        
        nav_layout.addWidget(prev_btn)
        nav_layout.addWidget(step_counter)
        nav_layout.addWidget(next_btn)
        nav_layout.addWidget(reset_btn)
        
        layout.addWidget(nav_container)
        
        # Scrollable area for static step descriptions
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("tutorialScrollArea")
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        
        # Static steps header
        static_header = QLabel("Complete Step-by-Step Solution:")
        static_header.setObjectName("staticStepsHeader")
        content_layout.addWidget(static_header)
        
        # Get example steps
        example_steps = self.get_example_steps(algo_name, category)
        
        # Add all static steps
        for step_num, (step_title, step_text) in enumerate(example_steps, 1):
            step_label = QLabel(f"Step {step_num}: {step_title}")
            step_label.setObjectName("stepTitle")
            content_layout.addWidget(step_label)
            
            step_content = QLabel(step_text)
            step_content.setObjectName("stepContent")
            step_content.setWordWrap(True)
            step_content.setTextFormat(Qt.RichText)
            content_layout.addWidget(step_content)
        
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        
        # Store interactive components for step navigation
        page.gantt_table = gantt_table
        page.step_explanation = step_explanation
        page.step_counter = step_counter
        page.prev_btn = prev_btn
        page.next_btn = next_btn
        page.current_step = 0
        # For FCFS, we have 4 processes, so 4 interactive steps (one per process execution)
        if category == "CPU" and "First Come First Served" in algo_name:
            page.total_steps = 4  # D, C, A, B
        else:
            page.total_steps = len(example_steps)
        page.example_steps = example_steps
        page.algo_name = algo_name
        page.category = category
        
        # Connect navigation buttons
        next_btn.clicked.connect(lambda: self.next_step(page))
        prev_btn.clicked.connect(lambda: self.prev_step(page))
        reset_btn.clicked.connect(lambda: self.reset_simulation(page))
        
        return page
    
    def get_example_content(self, algo_name, category):
        """Get example content for a specific algorithm
        Returns a list of tuples: (step_title, step_content)
        This is a placeholder - you can customize each example later
        """
        # Placeholder examples - you can replace these with actual step-by-step solutions
        if category == "CPU":
            if algo_name == "First Come First Served (FCFS)":
                return [
                    ("Order by Arrival Time", 
                     "In FCFS, processes are executed in the order they arrive in the ready queue.<br><br>"
                     "<b>Arrival Order:</b> D (arrives at 1) → C (arrives at 6) → A (arrives at 11) → B (arrives at 13)<br><br>"
                     "<b>Execution Order:</b> D → C → A → B"),
                    ("Process D Executes", 
                     "• <b>D arrives at time 1</b><br>"
                     "• D is the first process to arrive, so it starts immediately at time 1<br>"
                     "• Burst time = 6 units<br>"
                     "• <b>Executes from time 1 to 7</b><br>"
                     "• Completion Time = 7"),
                    ("Process C Executes", 
                     "• <b>C arrives at time 6</b><br>"
                     "• C waits 1 time unit (D finishes at 7, C arrived at 6)<br>"
                     "• Burst time = 9 units<br>"
                     "• <b>Executes from time 7 to 16</b><br>"
                     "• Completion Time = 16<br>"
                     "• Waiting Time = 7 - 6 = 1 unit"),
                    ("Process A Executes", 
                     "• <b>A arrives at time 11</b><br>"
                     "• A waits 5 time units (C finishes at 16, A arrived at 11)<br>"
                     "• Burst time = 8 units<br>"
                     "• <b>Executes from time 16 to 24</b><br>"
                     "• Completion Time = 24<br>"
                     "• Waiting Time = 16 - 11 = 5 units"),
                    ("Process B Executes", 
                     "• <b>B arrives at time 13</b><br>"
                     "• B waits 11 time units (A finishes at 24, B arrived at 13)<br>"
                     "• Burst time = 9 units<br>"
                     "• <b>Executes from time 24 to 33</b><br>"
                     "• Completion Time = 33<br>"
                     "• Waiting Time = 24 - 13 = 11 units"),
                    ("Calculate Performance Metrics", 
                     "<b>Turnaround Time = Completion Time - Arrival Time</b><br>"
                     "• D: 7 - 1 = <b>6</b><br>"
                     "• C: 16 - 6 = <b>10</b><br>"
                     "• A: 24 - 11 = <b>13</b><br>"
                     "• B: 33 - 13 = <b>20</b><br><br>"
                     "<b>Average Turnaround Time</b> = (6 + 10 + 13 + 20) / 4 = <b>12.25 units</b><br><br>"
                     "<b>Total Waiting Time</b> = 0 + 1 + 5 + 11 = <b>17 units</b><br>"
                     "<b>Average Waiting Time</b> = 17 / 4 = <b>4.25 units</b>")
                ]
            elif algo_name == "FCFS with Priority":
                return [
                    ("Understanding FCFS Priority (Preemptive)",
                     "FCFS with Priority is a preemptive algorithm where processes with higher priority (higher number) can preempt running processes.<br><br>"
                     "<b>Priority Order (higher = higher):</b> A(4) > D(3) > C(2) > B(1)<br>"
                     "<b>Arrival Times:</b> D(1), C(6), A(11), B(13)<br><br>"
                     "<b>Key Rule:</b> When a higher priority process arrives, it immediately preempts the current process."),
                    ("Time 1-7: Process D Executes",
                     "• <b>Time 1:</b> D arrives (priority=3), starts execution<br>"
                     "• D has burst time = 6 units<br>"
                     "• <b>Time 6:</b> C arrives (priority=2, lower than D's 3), no preemption<br>"
                     "• <b>D executes from time 1 to 7</b> and completes<br>"
                     "• Completion Time = 7"),
                    ("Time 7-11: Process C Starts Executing",
                     "• <b>Time 7:</b> D completes, ready queue has C<br>"
                     "• C has priority 2 (only process in queue)<br>"
                     "• C burst time = 9 units<br>"
                     "• <b>C executes from time 7 to 11</b> (4 units completed)<br>"
                     "• C remaining = 5 units<br>"
                     "• <b>Time 11:</b> A arrives (priority=4, highest priority!)"),
                    ("Time 11-19: Process A Preempts C",
                     "• <b>A has priority 4</b>, which is higher than C's priority 2<br>"
                     "• <b>Preemption!</b> A interrupts C immediately<br>"
                     "• C goes to ready queue with 5 units remaining<br>"
                     "• A burst time = 8 units<br>"
                     "• <b>Time 13:</b> B arrives (priority=1, lower than A), no preemption<br>"
                     "• <b>A executes from time 11 to 19</b> and completes all 8 units<br>"
                     "• Ready queue: [C with 5 left, B with 9]"),
                    ("Time 19-24: Process C Resumes and Completes",
                     "• <b>Time 19:</b> A completes, check ready queue<br>"
                     "• Ready queue priorities: C(2), B(1)<br>"
                     "• C has higher priority (2 > 1) → C resumes<br>"
                     "• <b>C executes from time 19 to 24</b> (5 remaining units)<br>"
                     "• <b>C completes at time 24</b><br>"
                     "• Completion Time = 24"),
                    ("Time 24-33: Process B Finally Executes",
                     "• <b>Time 24:</b> Only B remains in ready queue<br>"
                     "• B has been waiting since time 13<br>"
                     "• B has priority 1 (lowest)<br>"
                     "• <b>B executes from time 24 to 33</b> (all 9 units)<br>"
                     "• <b>B completes at time 33</b>"),
                    ("Final Results and Metrics",
                     "<b>Execution Timeline:</b><br>"
                     "D(1-7) → C(7-11) → A(11-19) → C(19-24) → B(24-33)<br><br>"
                     "<b>Completion Times:</b> D=7, C=24, A=19, B=33<br>"
                     "<b>Turnaround Times:</b><br>"
                     "• D: 7-1 = 6 | C: 24-6 = 18 | A: 19-11 = 8 | B: 33-13 = 20<br>"
                     "<b>Average Turnaround:</b> (6+18+8+20)/4 = 13 units<br><br>"
                     "<b>Note:</b> A (highest priority) got immediate CPU access, while B (lowest priority) waited the longest!")
                ]
            elif algo_name == "Shortest Job First (SJF)":
                return [
                    ("Select Process with Shortest Burst Time",
                     "In SJF, we always select the process with the shortest burst time from the ready queue.<br><br>"
                     "<b>Process Burst Times:</b> D=6, A=8, C=9, B=9<br><br>"
                     "<b>At time 1:</b> Only D has arrived → Execute D"),
                    ("Process D Executes",
                     "• <b>D arrives at time 1</b>, burst = 6<br>"
                     "• D is the only process ready at time 1<br>"
                     "• <b>Executes from time 1 to 7</b><br>"
                     "• Completion Time = 7"),
                    ("Process C Executes",
                     "• <b>At time 7:</b> Ready queue has just C <br>"
                     "• A has shorter burst time, but it isn't in the ready queue yet</b><br>"
                     "• <b>C executes from time 7 to 16</b><br>"
                     "• Completion Time = 16"),
                    ("Process A Executes",
                     "• <b>At time 16:</b> Ready queue has A (burst=8) and B (burst=9)<br>"
                     "• A has shorter burst time of 8 → Execute A<br>"
                     "• <b>A executes from time 16 to 24</b><br>"
                     "• Completion Time = 24"),
                    ("Process B Executes",
                     "• <b>At time 24:</b> Only B remains<br>"
                     "• B burst = 9<br>"
                     "• <b>B executes from time 24 to 33</b><br>"
                     "• Completion Time = 33"),
                    ("Final Results",
                     "<b>Execution Order (SJF):</b> D (6) → C (9) → A (8) → B (9)<br><br>"
                     "<b>Turnaround Times:</b><br>"
                     "• D: 7 - 1 = 6<br>"
                     "• C: 16 - 6 = 10<br>"
                     "• A: 24 - 11 = 13<br>"
                     "• B: 33 - 13 = 20<br><br>"
                     "<b>Average Turnaround Time:</b> (6+10+13+20)/4 = 12.25 units<br>"
                     "<b>Average Waiting Time:</b> (0+1+5+11)/4 = 4.25 units")
                ]
            elif algo_name == "Shortest Remaining Time (SRT)":
                return [
                    ("Understanding SRT (Preemptive SJF)",
                     "SRT is the preemptive version of SJF. At each time unit, we select the process with the shortest remaining burst time.<br><br>"
                     "<b>Initial Remaining Times:</b> D=6, C=9, A=8, B=9"),
                    ("Time 1-6: Process D Executes",
                     "• <b>Time 1:</b> D arrives (remaining=6), starts execution<br>"
                     "• <b>Time 6:</b> C arrives (remaining=9), but D has less (remaining=1) → Continue D<br>"
                     "• <b>D completes at time 7</b> (executed 6 units)"),
                    ("Time 7-11: Process C Executes",
                     "• <b>Time 7:</b> Only C is ready (remaining=9) → Execute C<br>"
                     "• C executes for 4 units (7 to 11)<br>"
                     "• <b>Time 11:</b> A arrives (remaining=8), C has remaining=5<br>"
                     "• <b>Preemption!</b> A has longer remaining time (8 > 5) → Continue C"),
                    ("Time 11-16: Process C Continues",
                     "• C continues execution (remaining went from 5 to 0)<br>"
                     "• <b>Time 13:</b> B arrives (remaining=9), C still has shortest (remaining=3)<br>"
                     "• <b>C completes at time 16</b>"),
                    ("Time 16-24: Process A Executes",
                     "• <b>Time 16:</b> Ready queue has A (remaining=8) and B (remaining=9)<br>"
                     "• A has shorter remaining time → Execute A<br>"
                     "• <b>A completes at time 24</b>"),
                    ("Time 24-33: Process B Executes",
                     "• <b>Time 24:</b> Only B remains (remaining=9)<br>"
                     "• <b>B completes at time 33</b>"),
                    ("Final Results",
                     "<b>Execution Timeline:</b> D(1-7) → C(7-16) → A(16-24) → B(24-33)<br><br>"
                     "<b>Note:</b> In this example, no actual preemption occurred because when C was running,<br>"
                     "new arrivals (A at 11, B at 13) had longer remaining times than C.<br><br>"
                     "<b>Completion Times:</b> D=7, C=16, A=24, B=33<br>"
                     "<b>Average Turnaround:</b> 12.25 units | <b>Average Waiting:</b> 4.25 units")
                ]
            elif algo_name == "Round Robin (RR)":
                return [
                    ("Understanding Round Robin (Time Quantum = 2)",
                     "Round Robin uses a time quantum (Q=2). Each process gets 2 time units before moving to the back of the queue.<br><br>"
                     "<b>Key Concept:</b> Ready State (RS) = Time when process becomes ready<br>"
                     "• Initially: RS = Arrival Time<br>"
                     "• After quantum: RS = Current Time when quantum ends"),
                    ("Time 1-3: Process D Gets Quantum",
                     "• <b>Time 1:</b> D arrives (RS=1), gets quantum of 2<br>"
                     "• D executes from time 1-3 (uses 2 units)<br>"
                     "• D remaining = 6-2 = 4, new RS = 3<br>"
                     "• Ready queue: [D with RS=3]"),
                    ("Time 3-5: Process D Gets Another Quantum",
                     "• <b>Time 3:</b> No new arrivals yet, D has earliest RS → D continues<br>"
                     "• D executes from time 3-5 (uses 2 more units)<br>"
                     "• D remaining = 4-2 = 2, new RS = 5<br>"
                     "• Ready queue: [D with RS=5]"),
                    ("Time 5-7: Process D Gets Third Quantum",
                     "• <b>Time 5:</b> No new arrivals, D continues<br>"
                     "• D executes from time 5-7 (uses 2 more units)<br>"
                     "• D remaining = 2-2 = 0 → <b>D completes!</b><br>"
                     "• Ready queue: []"),
                    ("Time 7-9: Process C Gets Quantum",
                     "• <b>Time 6:</b> C arrives (RS=6) but CPU is busy with D until time 7<br>"
                     "• <b>Time 7:</b> C gets quantum, executes from 7-9<br>"
                     "• C remaining = 9-2 = 7, new RS = 9<br>"
                     "• Ready queue: [C with RS=9]"),
                    ("Continue Pattern Until All Complete",
                     "The pattern continues with each process getting 2-unit time slices.<br><br>"
                     "<b>Execution continues:</b> C→C→C→A→C→B→A→B→A→B→A→B→C→B<br><br>"
                     "Round Robin ensures fair CPU time distribution among all processes."),
                ]
            elif algo_name == "Priority Scheduling":
                return [
                    ("Problem Statement", "Placeholder example for Priority Scheduling.<br><br>You can customize this with a detailed step-by-step solution."),
                ]
        
        elif category == "PRA":
            if algo_name == "First In First Out (FIFO)":
                return [
                    ("Problem Statement", "Placeholder example for FIFO page replacement.<br><br>You can customize this with a detailed step-by-step solution."),
                ]
            elif algo_name == "Least Recently Used (LRU)":
                return [
                    ("Problem Statement", "Placeholder example for LRU page replacement.<br><br>You can customize this with a detailed step-by-step solution."),
                ]
            elif algo_name == "Optimal Page Replacement":
                return [
                    ("Problem Statement", "Placeholder example for Optimal page replacement.<br><br>You can customize this with a detailed step-by-step solution."),
                ]
            elif algo_name == "Second Chance (Clock)":
                return [
                    ("Problem Statement", "Placeholder example for Second Chance algorithm.<br><br>You can customize this with a detailed step-by-step solution."),
                ]
        
        # Default fallback
        return [
            ("Example Coming Soon", f"A detailed step-by-step example for {algo_name} will be added here.")
        ]
    
    # CPU Scheduling Tutorial Content
    def get_fcfs_tutorial(self):
        return """
        <b>Overview:</b><br>
        First Come First Served (FCFS) is the simplest CPU scheduling algorithm. Processes are executed in the order they arrive in the ready queue.
        <br><br>
        <b>How it works:</b><br>
        • Processes are scheduled in order of arrival time<br>
        • Once a process starts executing, it runs to completion<br>
        • Non-preemptive (cannot be interrupted)<br>
        • Uses a simple FIFO (First In First Out) queue
        <br><br>
        <b>Advantages:</b><br>
        • Simple to understand and implement<br>
        • Fair - first come, first served<br>
        • No starvation
        <br><br>
        <b>Disadvantages:</b><br>
        • Convoy effect - short processes wait for long processes<br>
        • Poor average waiting time<br>
        • Not suitable for time-sharing systems
        """
    
    def get_sjf_tutorial(self):
        return """
        <b>Overview:</b><br>
        Shortest Job First (SJF) selects the process with the smallest burst time for execution next.
        <br><br>
        <b>How it works:</b><br>
        • Processes are sorted by burst time (shortest first)<br>
        • Ties are broken by arrival time<br>
        • Non-preemptive version waits for current process to complete<br>
        • Minimizes average waiting time
        <br><br>
        <b>Advantages:</b><br>
        • Optimal average waiting time<br>
        • Better throughput than FCFS<br>
        • Reduces waiting time for shorter processes
        <br><br>
        <b>Disadvantages:</b><br>
        • Requires knowledge of burst time (difficult in practice)<br>
        • Can cause starvation of long processes<br>
        • Not suitable for interactive systems
        """
    
    def get_srt_tutorial(self):
        return """
        <b>Overview:</b><br>
        Shortest Remaining Time (SRT) is the preemptive version of SJF. The process with the smallest remaining burst time is executed next.
        <br><br>
        <b>How it works:</b><br>
        • When a new process arrives, compare its burst time with remaining time of current process<br>
        • If new process has shorter remaining time, preempt current process<br>
        • Always executes the process with shortest remaining time<br>
        • Continuously updates as processes arrive
        <br><br>
        <b>Advantages:</b><br>
        • Better response time than SJF<br>
        • Optimal for minimizing average waiting time<br>
        • More responsive to short processes
        <br><br>
        <b>Disadvantages:</b><br>
        • Requires frequent context switching<br>
        • Long processes may starve<br>
        • Overhead from constant checking of remaining times
        """
    
    def get_rr_tutorial(self):
        return """
        <b>Overview:</b><br>
        Round Robin (RR) is designed for time-sharing systems. Each process gets a small unit of CPU time (quantum), then moves to the back of the queue.
        <br><br>
        <b>How it works:</b><br>
        • Each process gets a fixed time quantum (e.g., 2 time units)<br>
        • If process completes within quantum, it terminates<br>
        • If not, it's preempted and added to end of ready queue<br>
        • CPU cycles through all processes in circular order
        <br><br>
        <b>Advantages:</b><br>
        • Fair allocation of CPU time<br>
        • Good response time for interactive systems<br>
        • No starvation - all processes get CPU time<br>
        • Preemptive - can handle I/O bound processes
        <br><br>
        <b>Disadvantages:</b><br>
        • Average waiting time can be high<br>
        • Performance depends heavily on quantum size<br>
        • Context switching overhead<br>
        • Not optimal for varying burst times
        """
    
    def get_priority_tutorial(self):
        return """
        <b>Overview:</b><br>
        Priority Scheduling assigns a priority to each process. The CPU is allocated to the process with the highest priority.
        <br><br>
        <b>How it works:</b><br>
        • Each process has a priority value (higher value = higher priority)<br>
        • Process with highest priority executes first<br>
        • Can be preemptive or non-preemptive<br>
        • Ties broken by arrival time or FCFS
        <br><br>
        <b>Priority Assignment:</b><br>
        • Can be internal (based on time limits, memory requirements)<br>
        • Can be external (based on importance, user type)<br>
        • Static priorities don't change during execution<br>
        • Dynamic priorities can change based on behavior
        <br><br>
        <b>Advantages:</b><br>
        • Important processes get CPU first<br>
        • Flexible - can adapt to different needs<br>
        • Can be combined with other algorithms
        <br><br>
        <b>Disadvantages:</b><br>
        • Starvation - low priority processes may never execute<br>
        • Requires careful priority assignment<br>
        • Aging may be needed to prevent starvation
        """
    
    # PRA Tutorial Content
    def get_fifo_tutorial(self):
        return """
        <b>Overview:</b><br>
        First In First Out (FIFO) is the simplest page replacement algorithm. It replaces the oldest page in memory.
        <br><br>
        <b>How it works:</b><br>
        • Pages are organized in a queue based on arrival time<br>
        • When a page fault occurs and memory is full, replace the oldest page<br>
        • The page that has been in memory longest is replaced first<br>
        • Simple queue implementation
        <br><br>
        <b>Advantages:</b><br>
        • Simple to understand and implement<br>
        • Low overhead<br>
        • Fair - treats all pages equally
        <br><br>
        <b>Disadvantages:</b><br>
        • Can replace frequently used pages<br>
        • Suffers from Belady's Anomaly (more frames may cause more faults)<br>
        • Poor performance in practice<br>
        • Doesn't consider page usage patterns
        """
    
    def get_lru_tutorial(self):
        return """
        <b>Overview:</b><br>
        Least Recently Used (LRU) replaces the page that hasn't been used for the longest time.
        <br><br>
        <b>How it works:</b><br>
        • Tracks the time each page was last accessed<br>
        • On page fault, replace page with oldest access time<br>
        • Based on principle of temporal locality<br>
        • Requires tracking access history
        <br><br>
        <b>Advantages:</b><br>
        • Generally good performance<br>
        • Approximates optimal algorithm<br>
        • Doesn't suffer from Belady's Anomaly<br>
        • Reflects actual page usage
        <br><br>
        <b>Disadvantages:</b><br>
        • Expensive to implement perfectly<br>
        • Requires hardware support or approximation<br>
        • Overhead of tracking access times<br>
        • May need additional data structures
        """
    
    def get_optimal_tutorial(self):
        return """
        <b>Overview:</b><br>
        Optimal (OPT) page replacement replaces the page that won't be used for the longest time in the future.
        <br><br>
        <b>How it works:</b><br>
        • Looks ahead at future page references<br>
        • Replaces page that will be used farthest in the future<br>
        • Guarantees lowest possible page fault rate<br>
        • Theoretical benchmark for other algorithms
        <br><br>
        <b>Advantages:</b><br>
        • Optimal - lowest page fault rate possible<br>
        • Useful as benchmark for comparing algorithms<br>
        • Theoretically perfect performance
        <br><br>
        <b>Disadvantages:</b><br>
        • Impossible to implement in real systems<br>
        • Requires knowledge of future page references<br>
        • Only useful for analysis and comparison<br>
        • Cannot be used in practice
        """
    
    def get_second_chance_tutorial(self):
        return """
        <b>Overview:</b><br>
        Second Chance (Clock algorithm) is an improvement over FIFO that considers a reference bit.
        <br><br>
        <b>How it works:</b><br>
        • Maintains pages in circular queue (like a clock)<br>
        • Each page has a reference bit (0 or 1)<br>
        • When page is accessed, reference bit set to 1<br>
        • On page fault: check oldest page's reference bit<br>
        • If bit is 1, set to 0 and give it a "second chance"<br>
        • If bit is 0, replace the page
        <br><br>
        <b>Advantages:</b><br>
        • Better than pure FIFO<br>
        • Considers page usage<br>
        • Simple to implement<br>
        • Reasonable performance
        <br><br>
        <b>Disadvantages:</b><br>
        • Not as good as LRU<br>
        • May clear many reference bits before finding victim<br>
        • In worst case, behaves like FIFO
        """
