"""
Custom Sidebar Button Widget
"""

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt


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
