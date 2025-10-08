"""
Settings Page for theme selection and other application preferences
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox,
                              QGroupBox, QFormLayout, QScrollArea)
from PySide6.QtCore import Signal, QSettings
from themes.theme_manager import ThemeManager


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
