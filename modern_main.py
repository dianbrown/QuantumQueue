"""
Modern GUI Main Window with Sidebar Menu
Inspired by PyDracula design
"""

import sys
import os
from PySide6.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, QFrame, QStackedWidget,
                              QLabel, QSizePolicy, QComboBox, QGroupBox, QFormLayout,
                              QSpacerItem, QScrollArea)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QSize, Signal, QSettings
from PySide6.QtGui import QIcon, QFont, QPixmap, QPainter, QPen, QColor
from PySide6.QtSvg import QSvgRenderer

# Import the existing CPU scheduling app
from CPU.ui.main_window import CPUSchedulingApp
# Import the PRA app
from PRA.ui.main_window import PRAMainWindow
# Import the theme manager
from themes.theme_manager import ThemeManager


class CustomTitleBar(QFrame):
    """Custom title bar with window controls and app logo/name"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.dragging = False
        self.drag_position = None
        self.is_maximized = False  # Track maximize state
        
        # Set fixed height for title bar and use QFrame for isolation
        self.setFixedHeight(40)
        self.setFrameShape(QFrame.NoFrame)
        self.setObjectName("titleBarFrame")
        
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)
        
        # Left side - Logo and App Name
        left_widget = QWidget()
        left_layout = QHBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)
        
        # Logo
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(32, 26)
        self.logo_label.setScaledContents(True)
        # Try to load logo from icons folder
        logo_pixmap = QPixmap("Assets/Icons/QuantumQueue.png")
        if not logo_pixmap.isNull():
            self.logo_label.setPixmap(logo_pixmap)
        left_layout.addWidget(self.logo_label)
        
        # App name
        self.app_name = QLabel("QuantumQueue - CPU & PRA")
        self.app_name.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        left_layout.addWidget(self.app_name)
        
        layout.addWidget(left_widget)
        
        # Spacer to push buttons to the right
        layout.addStretch()
        
        # Right side - Window control buttons
        # Minimize button
        self.minimize_btn = QPushButton()
        self.minimize_btn.setIcon(QIcon("Assets/icons/minimize.png"))
        self.minimize_btn.setIconSize(QSize(16, 16))
        self.minimize_btn.setFixedSize(40, 40)
        self.minimize_btn.clicked.connect(self.minimize_window)
        self.minimize_btn.setCursor(Qt.PointingHandCursor)
        
        # Maximize/Restore button
        self.maximize_btn = QPushButton()
        self.maximize_btn.setIcon(QIcon("Assets/icons/maximize.png"))
        self.maximize_btn.setIconSize(QSize(16, 16))
        self.maximize_btn.setFixedSize(40, 40)
        self.maximize_btn.clicked.connect(self.maximize_restore_window)
        self.maximize_btn.setCursor(Qt.PointingHandCursor)
        
        # Close button
        self.close_btn = QPushButton()
        self.close_btn.setIcon(QIcon("Assets/icons/exit.png"))
        self.close_btn.setIconSize(QSize(16, 16))
        self.close_btn.setFixedSize(40, 40)
        self.close_btn.clicked.connect(self.close_window)
        self.close_btn.setCursor(Qt.PointingHandCursor)
        
        # Add buttons to layout
        layout.addWidget(self.minimize_btn)
        layout.addWidget(self.maximize_btn)
        layout.addWidget(self.close_btn)
        
        # Apply default style
        self.apply_default_style()
        
    def apply_default_style(self):
        """Apply default styling to title bar"""
        self.setStyleSheet("""
            QFrame#titleBarFrame {
                background-color: #23272a;
                border: none;
                border-bottom: 2px solid #40444b;
            }
            QFrame#titleBarFrame QWidget {
                background-color: transparent;
            }
        """)
        
        button_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                color: #dcddde;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #40444b;
            }
        """
        
        self.minimize_btn.setStyleSheet(button_style)
        self.maximize_btn.setStyleSheet(button_style)
        self.close_btn.setStyleSheet(button_style + """
            QPushButton:hover {
                background-color: #e74c3c;
                color: white;
            }
        """)
    
    def apply_theme_colors(self, theme: dict):
        """Apply theme colors to the title bar"""
        bg_color = theme.get('titlebar_bg', theme.get('sidebar_header_bg', '#23272a'))
        border_color = theme.get('sidebar_border', '#40444b')
        text_color = theme.get('text_primary', '#dcddde')
        hover_color = theme.get('sidebar_hover', '#40444b')
        
        # Apply stylesheet directly to the QFrame container
        self.setStyleSheet(f"""
            QFrame#titleBarFrame {{
                background-color: {bg_color};
                border: none;
                border-bottom: 2px solid {border_color};
            }}
            QFrame#titleBarFrame QWidget {{
                background-color: transparent;
            }}
        """)
        
        # Force update
        self.update()
        self.repaint()
        
        self.app_name.setStyleSheet(f"""
            QLabel {{
                color: {text_color};
                font-size: 14px;
                font-weight: bold;
            }}
        """)
        
        button_style = f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {text_color};
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """
        
        self.minimize_btn.setStyleSheet(button_style)
        self.maximize_btn.setStyleSheet(button_style)
        self.close_btn.setStyleSheet(button_style + """
            QPushButton:hover {
                background-color: #e74c3c;
                color: white;
            }
        """)
    
    def mousePressEvent(self, event):
        """Handle mouse press for window dragging"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.parent.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for window dragging"""
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.parent.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release to stop dragging"""
        self.dragging = False
        event.accept()
    
    def mouseDoubleClickEvent(self, event):
        """Handle double click to maximize/restore"""
        if event.button() == Qt.LeftButton:
            self.maximize_restore_window()
            event.accept()
    
    def minimize_window(self):
        """Minimize the window"""
        self.parent.showMinimized()
    
    def maximize_restore_window(self):
        """Toggle between maximized and normal window state"""
        if self.is_maximized:
            # Currently maximized, so restore to normal
            self.parent.showNormal()
            self.maximize_btn.setIcon(QIcon("Assets/icons/maximize.png"))
            self.is_maximized = False
        else:
            # Currently normal, so maximize
            self.parent.showMaximized()
            self.maximize_btn.setIcon(QIcon("Assets/icons/undock.png"))
            self.is_maximized = True
    
    def close_window(self):
        """Close the window"""
        self.parent.close()


class SidebarButton(QPushButton):
    """Custom sidebar button with icon and text"""
    
    def __init__(self, text="", icon_path="", parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                text-align: left;
                padding: 15px 20px;
                color: #c3c3c3;
                font-size: 14px;
                font-weight: normal;
            }
            QPushButton:hover {
                background-color: #40444b;
                color: white;
            }
            QPushButton:checked {
                background-color: #565b5e;
                color: white;
                border-left: 3px solid #1f5582;
            }
        """)


class CollapsibleSidebar(QFrame):
    """Collapsible sidebar menu"""
    
    menu_changed = Signal(int)  # Signal emitted when menu selection changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(60)  # Collapsed width
        self.expanded_width = 200
        self.collapsed_width = 60
        self.is_expanded = False
        
        self.setup_ui()
        self.setup_animation()
        
    def setup_ui(self):
        """Setup the sidebar UI"""
        self.setStyleSheet("""
            QFrame {
                background-color: #2c2f33;
                border: none;
                border-right: 1px solid #40444b;
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header with hamburger menu
        self.header = QFrame()
        self.header.setFixedHeight(60)
        self.header.setStyleSheet("background-color: #23272a; border-bottom: 1px solid #40444b;")
        
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(10, 10, 10, 10)
        
        # Hamburger menu button
        self.menu_btn = QPushButton()
        self.menu_btn.setFixedSize(40, 40)
        self.menu_btn.setIcon(QIcon("Assets/icons/menu.png"))
        self.menu_btn.setIconSize(QSize(24, 24))
        self.menu_btn.setCursor(Qt.PointingHandCursor)
        self.menu_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #40444b;
                border-radius: 5px;
            }
        """)
        self.menu_btn.clicked.connect(self.toggle_sidebar)
        
        header_layout.addWidget(self.menu_btn)
        header_layout.addStretch()
        
        layout.addWidget(self.header)
        
        # Menu items
        self.menu_frame = QFrame()
        menu_layout = QVBoxLayout(self.menu_frame)
        menu_layout.setContentsMargins(0, 20, 0, 0)
        menu_layout.setSpacing(5)
        
        # Home button
        self.home_btn = SidebarButton("Home", "Assets/icons/home.png")
        self.home_btn.setText("  Home" if self.is_expanded else "")
        self.home_btn.setIcon(QIcon("Assets/icons/home.png"))
        self.home_btn.setIconSize(QSize(20, 20))
        self.home_btn.clicked.connect(lambda: self.menu_changed.emit(0))
        self.home_btn.setChecked(True)  # Default selection
        menu_layout.addWidget(self.home_btn)
        
        # CPU Scheduling button
        self.cpu_btn = SidebarButton("CPU Scheduling", "Assets/icons/cpu.png")
        self.cpu_btn.setText("  CPU Scheduling" if self.is_expanded else "")
        self.cpu_btn.setIcon(QIcon("Assets/icons/cpu.png"))
        self.cpu_btn.setIconSize(QSize(20, 20))
        self.cpu_btn.clicked.connect(lambda: self.menu_changed.emit(1))
        menu_layout.addWidget(self.cpu_btn)
        
        # PRA button
        self.pra_btn = SidebarButton("Page Replacement", "Assets/icons/PRA.png")
        self.pra_btn.setText("  Page Replacement" if self.is_expanded else "")
        self.pra_btn.setIcon(QIcon("Assets/icons/PRA.png"))
        self.pra_btn.setIconSize(QSize(20, 20))
        self.pra_btn.clicked.connect(lambda: self.menu_changed.emit(2))
        menu_layout.addWidget(self.pra_btn)
        
        # Help button
        self.help_btn = SidebarButton("Help", "Assets/icons/help.png")
        self.help_btn.setText("  Help" if self.is_expanded else "")
        self.help_btn.setIcon(QIcon("Assets/icons/help.png"))
        self.help_btn.setIconSize(QSize(20, 20))
        self.help_btn.clicked.connect(lambda: self.menu_changed.emit(3))
        menu_layout.addWidget(self.help_btn)
        
        # Add stretch to push settings to bottom
        menu_layout.addStretch()
        
        # Settings button (at bottom)
        self.settings_btn = SidebarButton("Settings", "Assets/icons/settings.png")
        self.settings_btn.setText("  Settings" if self.is_expanded else "")
        self.settings_btn.setIcon(QIcon("Assets/icons/settings.png"))
        self.settings_btn.setIconSize(QSize(20, 20))
        self.settings_btn.clicked.connect(lambda: self.menu_changed.emit(4))
        menu_layout.addWidget(self.settings_btn)
        
        layout.addWidget(self.menu_frame)
        
        # Store buttons for easy access
        self.buttons = [self.home_btn, self.cpu_btn, self.pra_btn, self.help_btn, self.settings_btn]
        
    def setup_animation(self):
        """Setup the sidebar animation"""
        self.animation = QPropertyAnimation(self, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        
    def toggle_sidebar(self):
        """Toggle sidebar expanded/collapsed state"""
        if self.is_expanded:
            self.collapse_sidebar()
        else:
            self.expand_sidebar()
            
    def expand_sidebar(self):
        """Expand the sidebar"""
        self.is_expanded = True
        self.animation.setStartValue(self.collapsed_width)
        self.animation.setEndValue(self.expanded_width)
        self.animation.start()
        
        # Update button texts to show text with icons
        self.home_btn.setText("  Home")
        self.cpu_btn.setText("  CPU Scheduling")
        self.pra_btn.setText("  Page Replacement")
        self.help_btn.setText("  Help")
        self.settings_btn.setText("  Settings")
        
    def collapse_sidebar(self):
        """Collapse the sidebar"""
        self.is_expanded = False
        self.animation.setStartValue(self.expanded_width)
        self.animation.setEndValue(self.collapsed_width)
        self.animation.start()
        
        # Update button texts to show icons only
        self.home_btn.setText("")
        self.cpu_btn.setText("")
        self.pra_btn.setText("")
        self.help_btn.setText("")
        self.settings_btn.setText("")
        
    def set_active_button(self, index):
        """Set the active button"""
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i == index)


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
        self.cpu_btn = QPushButton("📚 CPU Scheduling Tutorials")
        self.cpu_btn.setObjectName("cpuTutorialBtn")
        self.cpu_btn.setCursor(Qt.PointingHandCursor)
        self.cpu_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        button_layout.addWidget(self.cpu_btn)
        
        # PRA Tutorial Button
        self.pra_btn = QPushButton("💾 Page Replacement Tutorials")
        self.pra_btn.setObjectName("praTutorialBtn")
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


class SettingsPage(QWidget):
    """Settings page with theme selection and other preferences"""
    
    theme_changed = Signal(str)  # Signal emitted when theme changes
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings()
        self.theme_manager = ThemeManager()
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """Setup the settings UI"""
        # Main layout with scroll area
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Scroll area for settings
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Title
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff; margin-bottom: 20px;")
        scroll_layout.addWidget(title)
        
        # Theme settings group
        theme_group = QGroupBox("Appearance")
        theme_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #72767d;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        theme_layout = QFormLayout(theme_group)
        theme_layout.setSpacing(15)
        
        # Theme selection
        self.theme_combo = QComboBox()
        available_themes = self.theme_manager.get_available_themes()
        if available_themes:
            self.theme_combo.addItems(available_themes)
        else:
            # Fallback if no themes are loaded
            self.theme_combo.addItems(["Dracula"])
        self.theme_combo.setStyleSheet("""
            QComboBox {
                background-color: #40444b;
                border: 1px solid #72767d;
                padding: 8px 12px;
                border-radius: 4px;
                color: white;
                font-size: 14px;
                min-width: 200px;
            }
            QComboBox:hover {
                border-color: #7289da;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #c3c3c3;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #40444b;
                border: 1px solid #72767d;
                selection-background-color: #7289da;
                color: white;
            }
        """)
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("color: #c3c3c3; font-size: 14px;")
        theme_layout.addRow(theme_label, self.theme_combo)
        
        scroll_layout.addWidget(theme_group)
        
        # Application settings group (placeholder for future settings)
        app_group = QGroupBox("Application")
        app_group.setStyleSheet(theme_group.styleSheet())
        app_layout = QFormLayout(app_group)
        
        # Placeholder for future settings
        placeholder_label = QLabel("More settings coming soon...")
        placeholder_label.setStyleSheet("color: #c3c3c3; font-style: italic; font-size: 14px;")
        app_layout.addWidget(placeholder_label)
        
        scroll_layout.addWidget(app_group)
        
        # Add stretch to push everything to the top
        scroll_layout.addStretch()
        
        # Setup scroll area
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        main_layout.addWidget(scroll_area)
        
    def on_theme_changed(self, theme_name):
        """Handle theme change"""
        self.settings.setValue("theme", theme_name)
        self.theme_changed.emit(theme_name)
        
    def load_settings(self):
        """Load saved settings"""
        saved_theme = self.settings.value("theme", "Dracula")
        if saved_theme:
            index = self.theme_combo.findText(saved_theme)
            if index >= 0:
                self.theme_combo.setCurrentIndex(index)


class ModernMainWindow(QMainWindow):
    """Main application window with modern sidebar"""
    
    def __init__(self):
        super().__init__()
        
        # Make window frameless with shadow
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        self.setWindowTitle("CPU Scheduling & Page Replacement Practice")
        self.setMinimumSize(1200, 800)
        
        # Variables for window resizing
        self.resizing = False
        self.resize_edge = None
        self.resize_margin = 5  # Pixels from edge to trigger resize
        
        # Initialize settings and theme manager
        self.settings = QSettings()
        self.theme_manager = ThemeManager()
        
        self.setup_ui()
        
        # Apply saved theme or default
        saved_theme = self.settings.value("theme", "Dracula")
        self.apply_theme(saved_theme)
        
    def setup_ui(self):
        """Setup the main UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout (vertical to accommodate title bar)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Add custom title bar
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        # Content layout (horizontal for sidebar and pages)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = CollapsibleSidebar()
        self.sidebar.menu_changed.connect(self.change_page)
        content_layout.addWidget(self.sidebar)
        
        # Content area
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("""
            QStackedWidget {
                background-color: #36393f;
                border: none;
            }
        """)
        
        # Add pages
        self.setup_pages()
        
        content_layout.addWidget(self.content_stack)
        
        # Add content layout to main layout
        main_layout.addLayout(content_layout)
        
    def setup_pages(self):
        """Setup the different pages"""
        # CPU Scheduling Page
        self.cpu_page = CPUSchedulingApp()
        self.cpu_page.setStyleSheet("""
            QWidget {
                background-color: #36393f;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #7289da;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #677bc4;
            }
            QComboBox {
                background-color: #40444b;
                border: 1px solid #72767d;
                padding: 5px;
                border-radius: 3px;
                color: white;
            }
            QTableWidget {
                background-color: #40444b;
                gridline-color: #72767d;
                border: 1px solid #72767d;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #2c2f33;
                color: white;
                padding: 5px;
                border: 1px solid #72767d;
            }
        """)
        self.content_stack.addWidget(self.cpu_page)
        
        # Home Page
        self.home_page = self.create_home_page()
        self.content_stack.addWidget(self.home_page)
        
        # CPU Page
        self.content_stack.addWidget(self.cpu_page)
        
        # PRA Page
        self.pra_page = PRAMainWindow()
        self.content_stack.addWidget(self.pra_page)
        
        # Help Page
        self.help_page = HelpPage()
        self.content_stack.addWidget(self.help_page)
        
        # Settings Page
        self.settings_page = SettingsPage()
        self.settings_page.theme_changed.connect(self.apply_theme)
        self.content_stack.addWidget(self.settings_page)
    
    def create_home_page(self):
        """Create the home page with logo and application information"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "Assets/Icons", "QuantumQueue.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            # Scale the logo to a reasonable size (max 400px width while maintaining aspect ratio)
            scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)
        
        # Add spacing
        layout.addSpacing(30)
        
        # Application Name
        app_name = QLabel("QuantumQueue")
        app_name.setObjectName("appTitle")
        app_name.setStyleSheet("""
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 10px;
        """)
        app_name.setAlignment(Qt.AlignCenter)
        layout.addWidget(app_name)
        
        # Subtitle
        subtitle = QLabel("CPU Scheduling and Page Replacement Algorithm Visualization")
        subtitle.setObjectName("appSubtitle")
        subtitle.setStyleSheet("""
            font-size: 20px;
            margin-bottom: 20px;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Add spacing
        layout.addSpacing(20)
        
        # Description
        description = QLabel(
            "Includes customizable settings, such as different themes in the settings.\n"
            "Tutorials for all algorithms are in the help section! \n\n"
            "The tutorials includes all the steps needed to complete the algorithms.\n"
            "No more having to rely on confusing videos or tutors!"
        )
        description.setObjectName("appDescription")
        description.setStyleSheet("""
            font-size: 16px;
            line-height: 1.6;
        """)
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Add spacing
        layout.addSpacing(30)
        
        # Creator info
        creator_info = QLabel("Created by Dian Brown")
        creator_info.setObjectName("appAuthor")
        creator_info.setStyleSheet("""
            font-size: 14px;
            font-style: italic;
        """)
        creator_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(creator_info)
        
        # Add stretch to push everything to center
        layout.addStretch()
        
        return page
    
    def create_placeholder_page(self, title, subtitle):
        """Create a placeholder page with title and subtitle"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #4a90e2;
            margin-bottom: 10px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("""
            font-size: 18px;
            color: #888;
        """)
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)
        
        return page
        
    def change_page(self, index):
        """Change the active page"""
        self.content_stack.setCurrentIndex(index)
        self.sidebar.set_active_button(index)
        
    def apply_theme(self, theme_name):
        """Apply the selected theme to the application"""
        # Get theme colors from theme manager
        theme = self.theme_manager.get_theme_colors(theme_name)
        
        # Fallback to default theme if theme not found
        if not theme:
            theme_name = "Dracula"
            theme = self.theme_manager.get_theme_colors(theme_name)
            
        # If still no theme found, use hardcoded fallback
        if not theme:
            theme = {
                "main_bg": "#36393f",
                "sidebar_bg": "#2c2f33", 
                "sidebar_header_bg": "#23272a",
                "sidebar_border": "#40444b",
                "titlebar_bg": "#23272a",
                "sidebar_hover": "#40444b",
                "sidebar_active": "#565b5e",
                "sidebar_accent": "#1f5582",
                "text_primary": "#ffffff",
                "text_secondary": "#c3c3c3",
                "button_bg": "#7289da",
                "button_hover": "#677bc4",
                "input_bg": "#40444b",
                "input_border": "#72767d",
                "table_bg": "#40444b",
                "table_grid": "#72767d",
                "header_bg": "#2c2f33",
                "results_box_bg": "#2b2b2b",
                "results_box_text": "#ffffff",
                "queue_container_bg": "#40444b",
                "queue_container_border": "#72767d",
                "queue_block_bg": "#7289da",
                "queue_block_border": "#677bc4",
                "queue_block_text": "#ffffff"
            }
        
        # Apply main window theme with modern scrollbars
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {theme['main_bg']};
                color: {theme['text_primary']};
            }}
            
            /* Modern Scrollbars - Horizontal */
            QScrollBar:horizontal {{
                border: none;
                background: {theme.get('scrollbar_bg', theme['input_bg'])};
                height: 8px;
                margin: 0px 21px 0 21px;
                border-radius: 0px;
            }}
            QScrollBar::handle:horizontal {{
                background: {theme.get('scrollbar_handle', theme['button_bg'])};
                min-width: 25px;
                border-radius: 4px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {theme.get('scrollbar_handle_hover', theme['button_hover'])};
            }}
            QScrollBar::add-line:horizontal {{
                border: none;
                background: {theme.get('scrollbar_border', theme['sidebar_border'])};
                width: 20px;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }}
            QScrollBar::sub-line:horizontal {{
                border: none;
                background: {theme.get('scrollbar_border', theme['sidebar_border'])};
                width: 20px;
                border-top-left-radius: 4px;
                border-bottom-left-radius: 4px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }}
            QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {{
                background: none;
            }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
            }}
            
            /* Modern Scrollbars - Vertical */
            QScrollBar:vertical {{
                border: none;
                background: {theme.get('scrollbar_bg', theme['input_bg'])};
                width: 8px;
                margin: 21px 0 21px 0;
                border-radius: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {theme.get('scrollbar_handle', theme['button_bg'])};
                min-height: 25px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {theme.get('scrollbar_handle_hover', theme['button_hover'])};
            }}
            QScrollBar::add-line:vertical {{
                border: none;
                background: {theme.get('scrollbar_border', theme['sidebar_border'])};
                height: 20px;
                border-bottom-left-radius: 4px;
                border-bottom-right-radius: 4px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }}
            QScrollBar::sub-line:vertical {{
                border: none;
                background: {theme.get('scrollbar_border', theme['sidebar_border'])};
                height: 20px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                background: none;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)
        
        # Apply sidebar theme
        self.sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {theme['sidebar_bg']};
                border: none;
                border-right: 1px solid {theme['sidebar_border']};
            }}
        """)
        
        # Update sidebar header
        self.sidebar.header.setStyleSheet(f"""
            background-color: {theme['sidebar_header_bg']}; 
            border-bottom: 1px solid {theme['sidebar_border']};
        """)
        
        # Update sidebar buttons
        button_style = f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                text-align: left;
                padding: 15px 20px;
                color: {theme['text_secondary']};
                font-size: 14px;
                font-weight: normal;
            }}
            QPushButton:hover {{
                background-color: {theme['sidebar_hover']};
                color: {theme['text_primary']};
            }}
            QPushButton:checked {{
                background-color: {theme['sidebar_active']};
                color: {theme['text_primary']};
                border-left: 3px solid {theme['sidebar_accent']};
            }}
        """
        
        for button in self.sidebar.buttons:
            button.setStyleSheet(button_style)
            
        # Update hamburger menu button
        self.sidebar.menu_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {theme['text_secondary']};
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {theme['sidebar_hover']};
                border-radius: 5px;
            }}
        """)
        
        # Apply CPU page theme
        self.cpu_page.setStyleSheet(f"""
            QWidget {{
                background-color: {theme['main_bg']};
                color: {theme['text_primary']};
            }}
            QLabel {{
                color: {theme['text_primary']};
            }}
            QPushButton {{
                background-color: {theme['button_bg']};
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                color: {theme['text_primary']};
                font-weight: bold;
                font-size: 12px;
                min-width: 70px;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: {theme['button_hover']};
            }}
            QComboBox {{
                background-color: {theme['input_bg']};
                border: 1px solid {theme['input_border']};
                padding: 5px;
                border-radius: 3px;
                color: {theme['text_primary']};
            }}
            QTableWidget {{
                background-color: {theme['table_bg']};
                gridline-color: {theme['table_grid']};
                border: 1px solid {theme['input_border']};
                color: {theme['text_primary']};
            }}
            QTableWidget::item {{
                padding: 5px;
            }}
            QHeaderView::section {{
                background-color: {theme['header_bg']};
                color: {theme['text_primary']};
                padding: 5px;
                border: 1px solid {theme['table_grid']};
            }}
        """)
        
        # Apply results box theme to CPU page
        if hasattr(self.cpu_page, 'results_label') and self.cpu_page.results_label:
            self.cpu_page.results_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {theme['results_box_bg']};
                    border: none;
                    padding: 10px;
                    font-family: monospace;
                    color: {theme['results_box_text']};
                }}
            """)
        
        if hasattr(self.cpu_page, 'results_scroll_area') and self.cpu_page.results_scroll_area:
            self.cpu_page.results_scroll_area.setStyleSheet(f"""
                QScrollArea {{
                    border: 1px solid {theme['input_border']};
                    border-radius: 5px;
                    background-color: {theme['results_box_bg']};
                }}
            """)
        
        # Apply scheduling block color to CPU page
        if hasattr(self.cpu_page, 'set_scheduling_block_color'):
            self.cpu_page.set_scheduling_block_color(theme['scheduling_block_bg'])
        
        # Apply PRA page theme  
        self.pra_page.setStyleSheet(f"""
            QWidget {{
                background-color: {theme['main_bg']};
                color: {theme['text_primary']};
            }}
            QLabel {{
                color: {theme['text_primary']};
            }}
            QPushButton {{
                background-color: {theme['button_bg']};
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                color: {theme['text_primary']};
                font-weight: bold;
                font-size: 12px;
                min-width: 70px;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: {theme['button_hover']};
            }}
            QComboBox {{
                background-color: {theme['input_bg']};
                border: 1px solid {theme['input_border']};
                padding: 5px;
                border-radius: 3px;
                color: {theme['text_primary']};
            }}
            QLineEdit {{
                background-color: {theme['input_bg']};
                border: 1px solid {theme['input_border']};
                padding: 5px;
                border-radius: 3px;
                color: {theme['text_primary']};
            }}
            QSpinBox {{
                background-color: {theme['input_bg']};
                border: 1px solid {theme['input_border']};
                padding: 5px;
                border-radius: 3px;
                color: {theme['text_primary']};
            }}
            QTableWidget {{
                background-color: {theme['table_bg']};
                gridline-color: {theme['table_grid']};
                border: 1px solid {theme['input_border']};
                color: {theme['text_primary']};
            }}
            QTableWidget::item {{
                padding: 5px;
            }}
            QHeaderView::section {{
                background-color: {theme['header_bg']};
                color: {theme['text_primary']};
                padding: 5px;
                border: 1px solid {theme['table_grid']};
            }}
        """)
        
        # Apply queue visualizer theme to PRA page
        if hasattr(self.pra_page, 'queue_widget') and self.pra_page.queue_widget:
            self.pra_page.queue_widget.set_theme_colors(theme)
        
        # Apply results box theme to PRA page
        if hasattr(self.pra_page, 'results_label') and self.pra_page.results_label:
            self.pra_page.results_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {theme['results_box_bg']};
                    border: none;
                    padding: 10px;
                    font-family: monospace;
                    color: {theme['results_box_text']};
                }}
            """)
        
        if hasattr(self.pra_page, 'results_scroll_area') and self.pra_page.results_scroll_area:
            self.pra_page.results_scroll_area.setStyleSheet(f"""
                QScrollArea {{
                    border: 1px solid {theme['input_border']};
                    border-radius: 5px;
                    background-color: {theme['results_box_bg']};
                }}
            """)
        
        # Apply Home page theme
        self.home_page.setStyleSheet(f"""
            QWidget {{
                background-color: {theme['main_bg']};
            }}
            QLabel {{
                background-color: transparent;
            }}
            QLabel#appTitle {{
                color: {theme.get('home_title', theme['button_bg'])};
            }}
            QLabel#appSubtitle {{
                color: {theme.get('home_subtitle', theme['text_secondary'])};
            }}
            QLabel#appDescription {{
                color: {theme.get('home_description', theme['text_secondary'])};
            }}
            QLabel#appAuthor {{
                color: {theme.get('home_author', theme['sidebar_accent'])};
            }}
        """)
        
        # Apply Help page theme
        if hasattr(self.help_page, 'apply_theme'):
            self.help_page.apply_theme(theme)
        
        # Update content stack
        self.content_stack.setStyleSheet(f"""
            QStackedWidget {{
                background-color: {theme['main_bg']};
                border: none;
            }}
        """)
        
        # Apply title bar theme LAST to ensure it's not overridden
        self.title_bar.apply_theme_colors(theme)
        
        # Save the theme setting
        self.settings.setValue("theme", theme_name)
        
        # Update the settings page combo box to reflect the current theme
        index = self.settings_page.theme_combo.findText(theme_name)
        if index >= 0:
            # Block signals to prevent triggering theme_changed signal
            self.settings_page.theme_combo.blockSignals(True)
            self.settings_page.theme_combo.setCurrentIndex(index)
            self.settings_page.theme_combo.blockSignals(False)
    
    def mousePressEvent(self, event):
        """Handle mouse press for window resizing"""
        if event.button() == Qt.LeftButton:
            self.resize_edge = self.get_resize_edge(event.position().toPoint())
            if self.resize_edge:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_geometry = self.geometry()
                event.accept()
                return
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for window resizing and cursor changes"""
        if self.resizing:
            self.perform_resize(event.globalPosition().toPoint())
            event.accept()
            return
        
        # Update cursor based on position
        edge = self.get_resize_edge(event.position().toPoint())
        if edge:
            self.update_cursor(edge)
        else:
            self.setCursor(Qt.ArrowCursor)
        
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release to stop resizing"""
        if event.button() == Qt.LeftButton:
            self.resizing = False
            self.resize_edge = None
            self.setCursor(Qt.ArrowCursor)
            event.accept()
        super().mouseReleaseEvent(event)
    
    def get_resize_edge(self, pos):
        """Determine which edge of the window is near the cursor"""
        rect = self.rect()
        margin = self.resize_margin
        
        left = pos.x() < margin
        right = pos.x() > rect.width() - margin
        top = pos.y() < margin
        bottom = pos.y() > rect.height() - margin
        
        if top and left:
            return "top-left"
        elif top and right:
            return "top-right"
        elif bottom and left:
            return "bottom-left"
        elif bottom and right:
            return "bottom-right"
        elif left:
            return "left"
        elif right:
            return "right"
        elif top:
            return "top"
        elif bottom:
            return "bottom"
        
        return None
    
    def update_cursor(self, edge):
        """Update the cursor based on the resize edge"""
        cursor_map = {
            "top": Qt.SizeVerCursor,
            "bottom": Qt.SizeVerCursor,
            "left": Qt.SizeHorCursor,
            "right": Qt.SizeHorCursor,
            "top-left": Qt.SizeFDiagCursor,
            "bottom-right": Qt.SizeFDiagCursor,
            "top-right": Qt.SizeBDiagCursor,
            "bottom-left": Qt.SizeBDiagCursor,
        }
        self.setCursor(cursor_map.get(edge, Qt.ArrowCursor))
    
    def perform_resize(self, global_pos):
        """Perform window resize based on edge"""
        if not self.resize_edge or self.isMaximized():
            return
        
        delta = global_pos - self.resize_start_pos
        geo = QRect(self.resize_start_geometry)
        
        min_width = self.minimumWidth()
        min_height = self.minimumHeight()
        
        if "left" in self.resize_edge:
            new_width = geo.width() - delta.x()
            if new_width >= min_width:
                geo.setLeft(geo.left() + delta.x())
        elif "right" in self.resize_edge:
            new_width = geo.width() + delta.x()
            if new_width >= min_width:
                geo.setWidth(new_width)
        
        if "top" in self.resize_edge:
            new_height = geo.height() - delta.y()
            if new_height >= min_height:
                geo.setTop(geo.top() + delta.y())
        elif "bottom" in self.resize_edge:
            new_height = geo.height() + delta.y()
            if new_height >= min_height:
                geo.setHeight(new_height)
        
        self.setGeometry(geo)


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("CPU Scheduling & PRA Practice")
    app.setOrganizationName("Dian Brown")
    app.setApplicationVersion("2.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    window = ModernMainWindow()
    
    # Set pointing hand cursor for all buttons in the application
    for widget in window.findChildren(QPushButton):
        widget.setCursor(Qt.PointingHandCursor)
    
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
