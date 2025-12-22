"""
Help Page with CPU Scheduling and Page Replacement Algorithm Tutorials
Modern card-based navigation with theme-consistent styling
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                              QStackedWidget, QScrollArea, QHBoxLayout,
                              QFrame, QGridLayout, QSizePolicy)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from resource_path import resource_path
from pages.FCFSTutorialPage import FCFSTutorialPage


class AlgorithmCard(QFrame):
    """A modern card widget for algorithm selection"""
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        self.setObjectName("algorithmCard")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(280, 140)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Centered title with larger font
        self.title_label = QLabel(title)
        self.title_label.setObjectName("cardTitle")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setWordWrap(True)
        layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
    
    def set_text_color(self, color):
        """Directly set the text color of the label"""
        self.title_label.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: bold; background: transparent;")


class HelpPage(QWidget):
    """Help page with tutorials for CPU Scheduling and Page Replacement Algorithms"""
    
    def __init__(self):
        super().__init__()
        self.current_theme = {}
        self.detail_pages = {}
        self.tutorial_pages = {}  # Store tutorial page references
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the help page UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)
        
        # Page 0: Main menu
        self.stack.addWidget(self._create_menu_page())
        
        # Page 1: CPU algorithms cards
        self.stack.addWidget(self._create_cpu_cards_page())
        
        # Page 2: PRA algorithms cards
        self.stack.addWidget(self._create_pra_cards_page())
        
        self.stack.setCurrentIndex(0)
    
    def _create_menu_page(self):
        """Create main menu with CPU and PRA options - List Format"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignCenter)
        
        # Title Section
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(10)
        
        self.menu_title = QLabel("Help & Tutorials")
        self.menu_title.setObjectName("helpMenuTitle")
        self.menu_title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(self.menu_title)
        
        self.menu_subtitle = QLabel("Select a category to explore algorithms")
        self.menu_subtitle.setObjectName("helpMenuSubtitle")
        self.menu_subtitle.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(self.menu_subtitle)
        
        layout.addWidget(title_container)
        layout.addSpacing(20)
        
        # List Buttons Container
        # CPU Button
        self.cpu_btn = QPushButton("  CPU Scheduling Algorithms")
        self.cpu_btn.setObjectName("menuListBtn")
        self.cpu_btn.setIcon(QIcon(resource_path("Assets/icons/CPU_Tutorial.png")))
        self.cpu_btn.setIconSize(QSize(48, 48))
        self.cpu_btn.setCursor(Qt.PointingHandCursor)
        self.cpu_btn.setMinimumHeight(100)
        self.cpu_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.cpu_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(self.cpu_btn)
        
        # PRA Button
        self.pra_btn = QPushButton("  Page Replacement Algorithms")
        self.pra_btn.setObjectName("menuListBtn")
        self.pra_btn.setIcon(QIcon(resource_path("Assets/icons/PRA_Tutorial.png")))
        self.pra_btn.setIconSize(QSize(48, 48))
        self.pra_btn.setCursor(Qt.PointingHandCursor)
        self.pra_btn.setMinimumHeight(100)
        self.pra_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pra_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        layout.addWidget(self.pra_btn)
        
        layout.addStretch()
        
        return page
    
    def _create_cpu_cards_page(self):
        """Create CPU algorithms card grid page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setObjectName("backBtn")
        back_btn.setMaximumWidth(100)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(back_btn)
        
        # Title
        self.cpu_title = QLabel("CPU Scheduling Algorithms")
        self.cpu_title.setObjectName("categoryTitle")
        layout.addWidget(self.cpu_title)
        
        layout.addSpacing(15)
        
        # Cards grid with smaller spacing
        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(12)
        
        # CPU Algorithms including priority variants
        cpu_algorithms = [
            "FCFS", "FCFS Priority", "SJF", 
            "SJF Priority", "SRT", "Round Robin", 
            "RR Priority"
        ]
        
        row, col = 0, 0
        for name in cpu_algorithms:
            card = AlgorithmCard(name)
            card.mousePressEvent = lambda e, n=name: self._show_detail(n, "CPU")
            grid.addWidget(card, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        layout.addWidget(grid_widget)
        layout.addStretch()
        
        return page
    
    def _create_pra_cards_page(self):
        """Create PRA algorithms card grid page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setObjectName("backBtn")
        back_btn.setMaximumWidth(100)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(back_btn)
        
        # Title
        self.pra_title = QLabel("Page Replacement Algorithms")
        self.pra_title.setObjectName("categoryTitle")
        layout.addWidget(self.pra_title)
        
        layout.addSpacing(15)
        
        # Cards grid with smaller spacing
        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(12)
        
        # PRA Algorithms
        pra_algorithms = ["FIFO", "LRU", "Optimal", "Second Chance", "Clock"]
        
        row, col = 0, 0
        for name in pra_algorithms:
            card = AlgorithmCard(name)
            card.mousePressEvent = lambda e, n=name: self._show_detail(n, "PRA")
            grid.addWidget(card, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        layout.addWidget(grid_widget)
        layout.addStretch()
        
        return page
    
    def _show_detail(self, algo_name, category):
        """Show algorithm detail page"""
        key = f"{category}_{algo_name}"
        
        if key not in self.detail_pages:
            page = self._create_detail_page(algo_name, category)
            self.detail_pages[key] = self.stack.count()
            self.stack.addWidget(page)
        
        self.stack.setCurrentIndex(self.detail_pages[key])
    
    def _create_detail_page(self, algo_name, category):
        """Create algorithm detail page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Back button
        back_idx = 1 if category == "CPU" else 2
        back_btn = QPushButton("Back to Algorithms")
        back_btn.setObjectName("backBtn")
        back_btn.setMaximumWidth(180)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(back_idx))
        layout.addWidget(back_btn)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("detailScrollArea")
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(15)
        
        # Title
        title = QLabel(algo_name)
        title.setObjectName("detailTitle")
        content_layout.addWidget(title)
        
        # Description
        desc = QLabel(self._get_description(algo_name))
        desc.setObjectName("detailDescription")
        desc.setWordWrap(True)
        desc.setTextFormat(Qt.RichText)
        content_layout.addWidget(desc)
        
        # Add "View Example" button for algorithms with tutorials
        if algo_name == "FCFS" and category == "CPU":
            example_btn = QPushButton("View Example")
            example_btn.setObjectName("exampleBtn")
            example_btn.setCursor(Qt.PointingHandCursor)
            example_btn.setMaximumWidth(200)
            example_btn.clicked.connect(lambda: self._show_tutorial("FCFS"))
            content_layout.addWidget(example_btn)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        return page
    
    def _show_tutorial(self, algo_name):
        """Show tutorial page for the specified algorithm"""
        if algo_name == "FCFS":
            if "FCFS" not in self.tutorial_pages:
                # Create and add the FCFS tutorial page
                tutorial = FCFSTutorialPage()
                tutorial.back_requested.connect(lambda: self.stack.setCurrentIndex(self.detail_pages.get("CPU_FCFS", 0)))
                self.tutorial_pages["FCFS"] = self.stack.count()
                self.stack.addWidget(tutorial)
                # Apply current theme if available
                if self.current_theme:
                    tutorial.apply_theme(self.current_theme)
            else:
                # Reset tutorial to first step when showing
                tutorial_index = self.tutorial_pages["FCFS"]
                tutorial_widget = self.stack.widget(tutorial_index)
                if tutorial_widget:
                    tutorial_widget.reset_tutorial()
            
            self.stack.setCurrentIndex(self.tutorial_pages["FCFS"])
    
    def _get_description(self, algo_name):
        """Get comprehensive algorithm description from AlgorithmRules"""
        descriptions = {
            # ==================== CPU SCHEDULING ====================
            "FCFS": """
                <h2>First Come First Served (FCFS)</h2>
                
                <h3>📖 How It Works</h3>
                <p>The simplest scheduling algorithm. Processes are executed in the exact order they arrive in the ready queue. Once a process starts running, it continues until it completes - no interruptions allowed.</p>
                
                <h3>📋 Algorithm Steps</h3>
                <ol>
                    <li>Sort all processes by arrival time</li>
                    <li>If two processes arrive at the same time, sort by Process ID</li>
                    <li>Execute each process completely before moving to the next</li>
                    <li>If CPU is idle (no process ready), wait until next arrival</li>
                </ol>
                
                <h3>⚠️ Edge Cases & Watch Out For</h3>
                <ul>
                    <li><b>Convoy Effect:</b> Short processes stuck waiting behind long ones</li>
                    <li><b>Idle Time:</b> If next process hasn't arrived yet, CPU sits idle</li>
                    <li><b>Tie-breaker:</b> When arrival times are equal, use Process ID (A before B)</li>
                    <li><b>Non-preemptive:</b> Once started, process CANNOT be interrupted</li>
                </ul>
            """,
            
            "FCFS Priority": """
                <h2>FCFS with Priority (Preemptive)</h2>
                
                <h3>📖 How It Works</h3>
                <p>FCFS with priority preemption. Higher priority processes can interrupt lower priority ones immediately. Within the same priority level, FCFS ordering applies based on Ready State time.</p>
                
                <h3>📋 Algorithm Steps</h3>
                <ol>
                    <li>When a process arrives, record its Ready State time</li>
                    <li>If new process has HIGHER priority than running process → preempt immediately</li>
                    <li>Among same priority: earliest Ready State time goes first</li>
                    <li>Preempted process gets NEW Ready State time = preemption time</li>
                </ol>
                
                <h3>⚠️ Edge Cases & Watch Out For</h3>
                <ul>
                    <li><b>Same Priority:</b> NO preemption - follow FCFS by Ready State</li>
                    <li><b>Priority Convention:</b> Higher number = Higher priority</li>
                    <li><b>Ready State Updates:</b> Preempted process gets NEW ready state time</li>
                    <li><b>Tie-breaker:</b> Ready State time → then Process ID</li>
                </ul>
            """,
            
            "SJF": """
                <h2>Shortest Job First (SJF)</h2>
                
                <h3>📖 How It Works</h3>
                <p>Selects the process with the shortest burst time from the ready queue. Non-preemptive - once a process starts, it runs to completion. Optimal for minimizing average waiting time.</p>
                
                <h3>📋 Algorithm Steps</h3>
                <ol>
                    <li>Add all arrived processes to the ready queue</li>
                    <li>Sort ready queue by: Burst Time → Arrival Time → Process ID</li>
                    <li>Select the first process (shortest burst) and run to completion</li>
                    <li>If no process is ready, advance time by 1</li>
                </ol>
                
                <h3>⚠️ Edge Cases & Watch Out For</h3>
                <ul>
                    <li><b>Starvation:</b> Long processes may never get CPU if short ones keep arriving</li>
                    <li><b>Same Burst Time:</b> Pick the one with earliest arrival</li>
                    <li><b>Same Burst + Arrival:</b> Use Process ID as final tie-breaker</li>
                    <li><b>Non-preemptive:</b> Running process cannot be interrupted</li>
                </ul>
            """,
            
            "SJF Priority": """
                <h2>SJF with Priority (Preemptive)</h2>
                
                <h3>📖 How It Works</h3>
                <p>Combines priority with SJF. A new process can preempt if it has higher priority OR same priority with shorter ORIGINAL burst time. Uses original burst for comparison, not remaining.</p>
                
                <h3>📋 Algorithm Steps</h3>
                <ol>
                    <li>Store ORIGINAL burst time for each process (never changes)</li>
                    <li>Check for preemption: higher priority OR (same priority AND shorter original burst)</li>
                    <li>Sort by: Priority (desc) → Original Burst (asc) → Arrival → ID</li>
                    <li>Execute for 1 time unit, repeat</li>
                </ol>
                
                <h3>⚠️ Edge Cases & Watch Out For</h3>
                <ul>
                    <li><b>CRITICAL:</b> Uses ORIGINAL burst, NOT remaining burst!</li>
                    <li><b>Preemption Check:</b> Both priority AND original burst matter</li>
                    <li><b>Same Priority + Same Burst:</b> Use arrival time, then Process ID</li>
                    <li><b>Remaining Burst:</b> Decreases, but comparison uses original</li>
                </ul>
            """,
            
            "SRT": """
                <h2>Shortest Remaining Time (SRT)</h2>
                
                <h3>📖 How It Works</h3>
                <p>Preemptive version of SJF. At any time, the process with the shortest REMAINING burst time runs. If a new process arrives with shorter remaining time, it preempts the current one.</p>
                
                <h3>📋 Algorithm Steps</h3>
                <ol>
                    <li>At each time unit, check all arrived processes</li>
                    <li>If new process has SHORTER remaining burst → preempt current</li>
                    <li>Sort ready queue by: Remaining Burst → Arrival → Process ID</li>
                    <li>Execute for 1 time unit, update remaining burst</li>
                </ol>
                
                <h3>⚠️ Edge Cases & Watch Out For</h3>
                <ul>
                    <li><b>EQUAL Remaining Time:</b> NO preemption - current process continues</li>
                    <li><b>SHORTER Remaining Time:</b> Preemption occurs immediately</li>
                    <li><b>Start Time:</b> First execution time is the start time (even after preemption)</li>
                    <li><b>Multiple Arrivals:</b> All added, then best is selected</li>
                </ul>
            """,
            
            "Round Robin": """
                <h2>Round Robin (RR)</h2>
                
                <h3>📖 How It Works</h3>
                <p>Each process gets a fixed time slice (quantum). When quantum expires, process moves to back of queue. Fair scheduling - all processes get CPU time. Uses "Ready State" to track eligibility.</p>
                
                <h3>📋 Algorithm Steps</h3>
                <ol>
                    <li>Set time quantum (default = 2)</li>
                    <li>Each process starts with Ready State = Arrival Time</li>
                    <li>Sort by: Ready State → Newest Arrival (most recent first)</li>
                    <li>Execute for min(quantum, remaining burst)</li>
                    <li>If burst remains: Update Ready State = current time, re-queue</li>
                </ol>
                
                <h3>⚠️ Edge Cases & Watch Out For</h3>
                <ul>
                    <li><b>Tie-breaker:</b> Same Ready State → pick NEWEST arrival (not oldest!)</li>
                    <li><b>Finishes Early:</b> If process completes before quantum, no re-queue</li>
                    <li><b>No Priority Preemption:</b> Only quantum expiration causes switch</li>
                    <li><b>New Arrivals:</b> Added to queue but don't preempt mid-quantum</li>
                </ul>
            """,
            
            "RR Priority": """
                <h2>Round Robin with Priority</h2>
                
                <h3>📖 How It Works</h3>
                <p>Round Robin with priority preemption. Higher priority processes can interrupt mid-quantum. Within same priority, normal RR rules apply. Combines fairness with priority handling.</p>
                
                <h3>📋 Algorithm Steps</h3>
                <ol>
                    <li>If new process has HIGHER priority → preempt immediately (even mid-quantum)</li>
                    <li>Filter to highest priority processes only</li>
                    <li>Among same priority: sort by Ready State → Newest Arrival</li>
                    <li>Execute for 1 time unit, track quantum usage</li>
                    <li>On quantum expire: update Ready State, move to queue</li>
                </ol>
                
                <h3>⚠️ Edge Cases & Watch Out For</h3>
                <ul>
                    <li><b>Priority Preemption:</b> Happens IMMEDIATELY, even mid-quantum</li>
                    <li><b>Same Priority:</b> No preemption, follow normal RR rules</li>
                    <li><b>Preempted Process:</b> Gets new Ready State and fresh quantum when resumed</li>
                    <li><b>Multiple High Priority:</b> Use Ready State among them</li>
                </ul>
            """,
            
            # ==================== PAGE REPLACEMENT ====================
            "FIFO": """
                <h2>First In First Out (FIFO)</h2>
                
                <h3>📖 How It Works</h3>
                <p>The simplest page replacement algorithm. Replaces the page that has been in memory the longest (first loaded). Uses a queue - oldest at front, newest at back.</p>
                
                <h3>📋 Algorithm Steps</h3>
                <ol>
                    <li>Sort frames by load time to establish queue order</li>
                    <li>On PAGE HIT: No change to queue (just mark hit)</li>
                    <li>On PAGE FAULT: Remove front of queue (oldest), add new page to back</li>
                    <li>The replaced frame moves to back of queue</li>
                </ol>
                
                <h3>⚠️ Edge Cases & Watch Out For</h3>
                <ul>
                    <li><b>Page Hit:</b> Queue order does NOT change</li>
                    <li><b>Belady's Anomaly:</b> More frames can cause MORE faults!</li>
                    <li><b>Same Load Time:</b> Use frame ID as tie-breaker</li>
                    <li><b>Doesn't Track Usage:</b> Frequently used pages can be replaced</li>
                </ul>
            """,
            
            "LRU": """
                <h2>Least Recently Used (LRU)</h2>
                
                <h3>📖 How It Works</h3>
                <p>Replaces the page that hasn't been USED for the longest time. Tracks actual page access, not just load time. On every access (hit or fault), the page becomes "most recently used".</p>
                
                <h3>📋 Algorithm Steps</h3>
                <ol>
                    <li>Initial order: sort by load time (oldest = LRU)</li>
                    <li>On PAGE HIT: Move accessed page to MRU position (back of queue)</li>
                    <li>On PAGE FAULT: Replace LRU page (front of queue)</li>
                    <li>New page goes to MRU position (back)</li>
                </ol>
                
                <h3>⚠️ Edge Cases & Watch Out For</h3>
                <ul>
                    <li><b>CRITICAL:</b> Hits UPDATE the queue order (unlike FIFO)</li>
                    <li><b>Multiple Hits:</b> Each hit refreshes position to MRU</li>
                    <li><b>LRU Page:</b> Always at FRONT of queue after all updates</li>
                    <li><b>Good Performance:</b> Approximates optimal without future knowledge</li>
                </ul>
            """,
            
            "Optimal": """
                <h2>Optimal (OPT / Farthest in Future)</h2>
                
                <h3>📖 How It Works</h3>
                <p>Replaces the page that won't be used for the longest time in the FUTURE. Requires knowing the entire page sequence in advance. Theoretical best - used as benchmark.</p>
                
                <h3>📋 Algorithm Steps</h3>
                <ol>
                    <li>On PAGE HIT: No change needed</li>
                    <li>On PAGE FAULT: For each page in memory, find next use in future</li>
                    <li>Select page with FARTHEST next use (or never used again)</li>
                    <li>If tie: choose lowest frame number</li>
                </ol>
                
                <h3>⚠️ Edge Cases & Watch Out For</h3>
                <ul>
                    <li><b>Never Used Again:</b> Distance = infinity (highest priority for replacement)</li>
                    <li><b>Multiple "Never Used":</b> Pick LOWEST frame number</li>
                    <li><b>Same Future Distance:</b> Pick lowest frame number</li>
                    <li><b>Not Practical:</b> Requires future knowledge - benchmark only</li>
                </ul>
            """,
            
            "Second Chance": """
                <h2>Second Chance (Enhanced FIFO)</h2>
                
                <h3>📖 How It Works</h3>
                <p>FIFO with a reference bit (R-bit). Pages with R-bit=1 get a "second chance" instead of being replaced. R-bit is set on access and cleared when given second chance.</p>
                
                <h3>📋 Algorithm Steps</h3>
                <ol>
                    <li>Initialize all R-bits = 1</li>
                    <li>On PAGE HIT: Set R-bit = 1 for that page</li>
                    <li>On PAGE FAULT: If ALL R-bits = 1, reset ALL to 0 first</li>
                    <li>Check front of queue: R-bit=0 → replace; R-bit=1 → set to 0, move to back</li>
                    <li>New page gets R-bit = 1</li>
                </ol>
                
                <h3>⚠️ Edge Cases & Watch Out For</h3>
                <ul>
                    <li><b>All R-bits = 1:</b> Reset ALL to 0, then first in queue is victim</li>
                    <li><b>Page Hit:</b> Only updates R-bit, queue order unchanged</li>
                    <li><b>Second Chance:</b> Page moves to back with R-bit = 0</li>
                    <li><b>Hit Before Eviction:</b> R-bit resets to 1</li>
                </ul>
            """,
            
            "Clock": """
                <h2>Clock (Circular Buffer)</h2>
                
                <h3>📖 How It Works</h3>
                <p>Circular implementation of Second Chance. Uses a clock hand pointer that sweeps around frames. Frames don't move - pointer moves. More efficient than Second Chance queue.</p>
                
                <h3>📋 Algorithm Steps</h3>
                <ol>
                    <li>Create circular frame order (highest ID first, then ascending)</li>
                    <li>Pointer starts at frame with oldest load time</li>
                    <li>On PAGE HIT: Set R-bit = 1, pointer stays</li>
                    <li>On PAGE FAULT: If all R-bits = 1, reset all to 0</li>
                    <li>Sweep: R-bit=1 → clear and advance; R-bit=0 → replace, advance</li>
                </ol>
                
                <h3>⚠️ Edge Cases & Watch Out For</h3>
                <ul>
                    <li><b>First Fault:</b> Reset all R-bits to 0, select at pointer</li>
                    <li><b>All R-bits = 1:</b> Reset ALL, victim is at current pointer</li>
                    <li><b>Page Hit:</b> Only R-bit update, pointer UNCHANGED</li>
                    <li><b>Pointer Wraps:</b> index = (index + 1) % num_frames</li>
                </ul>
            """,
        }
        return descriptions.get(algo_name, f"<p>Description for {algo_name}</p>")
    
    def apply_theme(self, theme: dict):
        """Apply theme colors - double outline artistic style"""
        self.current_theme = theme
        
        card_color = theme.get('button_bg', '#7289da')
        text_color = theme['text_primary']
        
        # Directly set text color on all algorithm cards
        for i in range(self.stack.count()):
            page = self.stack.widget(i)
            if page:
                cards = page.findChildren(AlgorithmCard)
                for card in cards:
                    card.set_text_color(text_color)
        
        # Apply theme to tutorial pages
        for algo_name, page_index in self.tutorial_pages.items():
            tutorial_widget = self.stack.widget(page_index)
            if tutorial_widget and hasattr(tutorial_widget, 'apply_theme'):
                tutorial_widget.apply_theme(theme)
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {theme['main_bg']};
                color: {text_color};
            }}
            
            /* Algorithm Cards - Double Outline "Artistic" Style */
            QFrame#algorithmCard {{
                background-color: transparent;
                border: 4px double {card_color};
                border-radius: 16px;
            }}
            
            QFrame#algorithmCard:hover {{
                background-color: {card_color};
                border: 4px solid {card_color};
            }}
            
            /* Card Text - Use text_primary for all labels in cards */
            QFrame#algorithmCard QLabel {{
                color: {text_color};
                font-size: 20px;
                font-weight: bold;
                background-color: transparent;
            }}
            
            QLabel#cardTitle {{
                color: {text_color};
            }}
            
            QFrame#algorithmCard:hover QLabel {{
                color: {theme.get('button_text', '#ffffff')};
            }}
            
            /* Menu page */
            QLabel#helpMenuTitle {{
                font-size: 36px;
                font-weight: bold;
                color: {text_color};
                background-color: transparent;
            }}
            
            QLabel#helpMenuSubtitle {{
                font-size: 18px;
                color: {theme['text_secondary']};
                background-color: transparent;
            }}
            
            /* Menu List Buttons */
            QPushButton#menuListBtn {{
                background-color: {card_color};
                border: none;
                padding: 20px 40px;
                border-radius: 16px;
                color: {theme.get('button_text', '#ffffff')};
                font-size: 22px;
                font-weight: bold;
                text-align: left;
                padding-left: 60px;
            }}
            
            QPushButton#menuListBtn:hover {{
                background-color: {theme.get('button_hover', '#677bc4')};
            }}

            /* Category pages */
            QLabel#categoryTitle {{
                font-size: 28px;
                font-weight: bold;
                color: {theme['text_primary']};
                background-color: transparent;
            }}
            
            /* Back button */
            QPushButton#backBtn {{
                background-color: {theme.get('input_bg', '#40444b')};
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                color: {theme['text_primary']};
                font-size: 14px;
            }}
            
            QPushButton#backBtn:hover {{
                background-color: {theme.get('sidebar_hover', '#4a4f56')};
            }}
            
            /* View Example button */
            QPushButton#exampleBtn {{
                background-color: {card_color};
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                color: {theme.get('button_text', '#ffffff')};
                font-size: 16px;
                font-weight: bold;
                margin-top: 15px;
            }}
            
            QPushButton#exampleBtn:hover {{
                background-color: {theme.get('button_hover', '#677bc4')};
            }}
            
            /* Detail page */
            QLabel#detailTitle {{
                font-size: 32px;
                font-weight: bold;
                color: {card_color};
                background-color: transparent;
            }}
            
            QLabel#detailDescription {{
                font-size: 15px;
                color: {theme['text_primary']};
                background-color: transparent;
                line-height: 1.5;
            }}
            
            QScrollArea#detailScrollArea {{
                border: none;
                background-color: transparent;
            }}
        """)
