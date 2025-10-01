"""
Modern GUI Main Window with Sidebar Menu
Inspired by PyDracula design
"""

import sys
from PySide6.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, QFrame, QStackedWidget,
                              QLabel, QSizePolicy, QComboBox, QGroupBox, QFormLayout,
                              QSpacerItem, QScrollArea)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QSize, Signal, QSettings
from PySide6.QtGui import QIcon, QFont, QPixmap, QPainter, QPen
from PySide6.QtSvg import QSvgRenderer

# Import the existing CPU scheduling app
from CPU.ui.main_window import CPUSchedulingApp
# Import the PRA app
from PRA.ui.main_window import PRAMainWindow
# Import the theme manager
from themes.theme_manager import ThemeManager


class SidebarButton(QPushButton):
    """Custom sidebar button with icon and text"""
    
    def __init__(self, text="", icon_path="", parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setCheckable(True)
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
        self.menu_btn.setText("☰")
        self.menu_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #c3c3c3;
                font-size: 18px;
                font-weight: bold;
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
        
        # CPU Scheduling button
        self.cpu_btn = SidebarButton("CPU Scheduling", "icons/cil-devices.png")
        self.cpu_btn.setText("  CPU Scheduling" if self.is_expanded else "")
        self.cpu_btn.setIcon(QIcon("icons/cil-devices.png"))
        self.cpu_btn.setIconSize(QSize(20, 20))
        self.cpu_btn.clicked.connect(lambda: self.menu_changed.emit(0))
        self.cpu_btn.setChecked(True)  # Default selection
        menu_layout.addWidget(self.cpu_btn)
        
        # PRA button
        self.pra_btn = SidebarButton("Page Replacement", "icons/cil-description.png")
        self.pra_btn.setText("  Page Replacement" if self.is_expanded else "")
        self.pra_btn.setIcon(QIcon("icons/cil-description.png"))
        self.pra_btn.setIconSize(QSize(20, 20))
        self.pra_btn.clicked.connect(lambda: self.menu_changed.emit(1))
        menu_layout.addWidget(self.pra_btn)
        
        # Settings button
        self.settings_btn = SidebarButton("Settings", "icons/icon_settings.png")
        self.settings_btn.setText("  Settings" if self.is_expanded else "")
        self.settings_btn.setIcon(QIcon("icons/icon_settings.png"))
        self.settings_btn.setIconSize(QSize(20, 20))
        self.settings_btn.clicked.connect(lambda: self.menu_changed.emit(2))
        menu_layout.addWidget(self.settings_btn)
        
        menu_layout.addStretch()
        layout.addWidget(self.menu_frame)
        
        # Store buttons for easy access
        self.buttons = [self.cpu_btn, self.pra_btn, self.settings_btn]
        
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
        self.cpu_btn.setText("  CPU Scheduling")
        self.pra_btn.setText("  Page Replacement")
        self.settings_btn.setText("  Settings")
        
    def collapse_sidebar(self):
        """Collapse the sidebar"""
        self.is_expanded = False
        self.animation.setStartValue(self.expanded_width)
        self.animation.setEndValue(self.collapsed_width)
        self.animation.start()
        
        # Update button texts to show icons only
        self.cpu_btn.setText("")
        self.pra_btn.setText("")
        self.settings_btn.setText("")
        
    def set_active_button(self, index):
        """Set the active button"""
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i == index)


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
            self.theme_combo.addItems(["Dark Theme (Default)"])
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
            QScrollBar:vertical {
                background-color: #40444b;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #72767d;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #7289da;
            }
        """)
        
        main_layout.addWidget(scroll_area)
        
    def on_theme_changed(self, theme_name):
        """Handle theme change"""
        self.settings.setValue("theme", theme_name)
        self.theme_changed.emit(theme_name)
        
    def load_settings(self):
        """Load saved settings"""
        saved_theme = self.settings.value("theme", "Dark Theme (Default)")
        if saved_theme:
            index = self.theme_combo.findText(saved_theme)
            if index >= 0:
                self.theme_combo.setCurrentIndex(index)


class ModernMainWindow(QMainWindow):
    """Main application window with modern sidebar"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPU Scheduling & Page Replacement Practice")
        self.setMinimumSize(1200, 800)
        
        # Initialize settings and theme manager
        self.settings = QSettings()
        self.theme_manager = ThemeManager()
        
        self.setup_ui()
        
        # Apply saved theme or default
        saved_theme = self.settings.value("theme", "Dark Theme (Default)")
        self.apply_theme(saved_theme)
        
    def setup_ui(self):
        """Setup the main UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = CollapsibleSidebar()
        self.sidebar.menu_changed.connect(self.change_page)
        main_layout.addWidget(self.sidebar)
        
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
        
        main_layout.addWidget(self.content_stack)
        
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
        
        # PRA Page
        self.pra_page = PRAMainWindow()
        self.content_stack.addWidget(self.pra_page)
        
        # Settings Page
        self.settings_page = SettingsPage()
        self.settings_page.theme_changed.connect(self.apply_theme)
        self.content_stack.addWidget(self.settings_page)
        
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
            theme_name = "Dark Theme (Default)"
            theme = self.theme_manager.get_theme_colors(theme_name)
            
        # If still no theme found, use hardcoded fallback
        if not theme:
            theme = {
                "main_bg": "#36393f",
                "sidebar_bg": "#2c2f33", 
                "sidebar_header_bg": "#23272a",
                "sidebar_border": "#40444b",
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
                "header_bg": "#2c2f33"
            }
        
        # Apply main window theme
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {theme['main_bg']};
                color: {theme['text_primary']};
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
        
        # Update content stack
        self.content_stack.setStyleSheet(f"""
            QStackedWidget {{
                background-color: {theme['main_bg']};
                border: none;
            }}
        """)
        
        # Save the theme setting
        self.settings.setValue("theme", theme_name)


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("CPU Scheduling & PRA Practice")
    app.setOrganizationName("Your Name")
    app.setApplicationVersion("2.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    window = ModernMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
