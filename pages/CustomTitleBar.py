"""
Custom Title Bar with window controls and drag functionality
"""

from PySide6.QtWidgets import (QFrame, QHBoxLayout, QWidget, QLabel, QPushButton)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
from resource_path import resource_path


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
        logo_pixmap = QPixmap(resource_path("Assets/Icons/QuantumQueue2.png"))
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
        self.minimize_btn.setIcon(QIcon(resource_path("Assets/icons/minimize.png")))
        self.minimize_btn.setIconSize(QSize(16, 16))
        self.minimize_btn.setFixedSize(40, 40)
        self.minimize_btn.clicked.connect(self.minimize_window)
        self.minimize_btn.setCursor(Qt.PointingHandCursor)
        
        # Maximize/Restore button
        self.maximize_btn = QPushButton()
        self.maximize_btn.setIcon(QIcon(resource_path("Assets/icons/maximize.png")))
        self.maximize_btn.setIconSize(QSize(16, 16))
        self.maximize_btn.setFixedSize(40, 40)
        self.maximize_btn.clicked.connect(self.maximize_restore_window)
        self.maximize_btn.setCursor(Qt.PointingHandCursor)
        
        # Close button
        self.close_btn = QPushButton()
        self.close_btn.setIcon(QIcon(resource_path("Assets/icons/exit.png")))
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
            self.maximize_btn.setIcon(QIcon(resource_path("Assets/icons/maximize.png")))
            self.is_maximized = False
        else:
            # Currently normal, so maximize
            self.parent.showMaximized()
            self.maximize_btn.setIcon(QIcon(resource_path("Assets/icons/undock.png")))
            self.is_maximized = True
    
    def close_window(self):
        """Close the window"""
        self.parent.close()
