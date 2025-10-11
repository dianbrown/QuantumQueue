"""
Collapsible Sidebar Menu Widget
"""

from PySide6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QPushButton)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QIcon
from pages.SideBarButton import SidebarButton


class CollapsibleSidebar(QFrame):
    """Collapsible sidebar menu"""
    
    menu_changed = Signal(int)  # Signal emitted when menu selection changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Don't use setFixedWidth - use setMaximumWidth and setMinimumWidth instead
        self.expanded_width = 200
        self.collapsed_width = 60
        self.is_expanded = False
        
        # Set initial width constraints (not fixed)
        self.setMinimumWidth(self.collapsed_width)
        self.setMaximumWidth(self.collapsed_width)
        
        # Ensure the sidebar can receive mouse events
        self.setAttribute(Qt.WA_NoMousePropagation, False)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        
        self.setup_ui()
        self.setup_animation()
        
    def setup_ui(self):
        """Setup the sidebar UI"""
        # Ensure sidebar stays on top
        self.raise_()
        
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
        self.menu_btn.setFocusPolicy(Qt.StrongFocus)
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
        self.menu_btn.clicked.connect(self.on_menu_clicked)
        
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
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        
        self.animation2 = QPropertyAnimation(self, b"maximumWidth")
        self.animation2.setDuration(300)
        self.animation2.setEasingCurve(QEasingCurve.Type.InOutQuart)
    
    def on_menu_clicked(self):
        """Handle menu button click - ensure sidebar is clickable"""
        self.raise_()
        self.toggle_sidebar()
    
    def toggle_sidebar(self):
        """Toggle sidebar expanded/collapsed state"""
        self.raise_()  # Ensure sidebar is on top when toggling
        if self.is_expanded:
            self.collapse_sidebar()
        else:
            self.expand_sidebar()
            
    def expand_sidebar(self):
        """Expand the sidebar"""
        self.is_expanded = True
        
        # Animate both minimum and maximum width
        self.animation.setStartValue(self.collapsed_width)
        self.animation.setEndValue(self.expanded_width)
        self.animation.start()
        
        self.animation2.setStartValue(self.collapsed_width)
        self.animation2.setEndValue(self.expanded_width)
        self.animation2.start()
        
        # Update button texts to show text with icons
        self.home_btn.setText("  Home")
        self.cpu_btn.setText("  CPU Scheduling")
        self.pra_btn.setText("  Page Replacement")
        self.help_btn.setText("  Help")
        self.settings_btn.setText("  Settings")
        
    def collapse_sidebar(self):
        """Collapse the sidebar"""
        self.is_expanded = False
        
        # Animate both minimum and maximum width
        self.animation.setStartValue(self.expanded_width)
        self.animation.setEndValue(self.collapsed_width)
        self.animation.start()
        
        self.animation2.setStartValue(self.expanded_width)
        self.animation2.setEndValue(self.collapsed_width)
        self.animation2.start()
        
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
