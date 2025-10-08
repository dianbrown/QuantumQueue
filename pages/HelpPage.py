"""
Help Page with CPU Scheduling and Page Replacement Algorithm Tutorials
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                              QStackedWidget, QScrollArea, QGroupBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize


class HelpPage(QWidget):
    """Help page with tutorials for CPU Scheduling and Page Replacement Algorithms"""
    
    def __init__(self):
        super().__init__()
        self.current_theme = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the help page UI"""
        # Main layout with stack for switching between menu and tutorials
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Stacked widget to switch between main menu and tutorial pages
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)
        
        # Create main menu page
        self.menu_page = self.create_menu_page()
        self.stack.addWidget(self.menu_page)
        
        # Create CPU scheduling tutorial page
        self.cpu_tutorial_page = self.create_cpu_tutorial_page()
        self.stack.addWidget(self.cpu_tutorial_page)
        
        # Create PRA tutorial page
        self.pra_tutorial_page = self.create_pra_tutorial_page()
        self.stack.addWidget(self.pra_tutorial_page)
        
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
                color: {theme['text_primary']};
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
                color: {theme['text_primary']};
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
        """)
    
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
