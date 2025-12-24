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
        self.current_theme = {}  # Store current theme for reference
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """Setup the settings UI"""
        # Main layout with scroll area
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Scroll area for settings
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(self.scroll_widget)
        
        # Title
        self.title = QLabel("Settings")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff; margin-bottom: 20px;")
        scroll_layout.addWidget(self.title)
        
        # Theme settings group
        self.theme_group = QGroupBox("Appearance")
        self.theme_group.setStyleSheet("""
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
        
        theme_layout = QFormLayout(self.theme_group)
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
        
        self.theme_label = QLabel("Theme:")
        self.theme_label.setStyleSheet("color: #c3c3c3; font-size: 14px;")
        theme_layout.addRow(self.theme_label, self.theme_combo)
        
        scroll_layout.addWidget(self.theme_group)
        
        # Application settings group (placeholder for future settings)
        self.app_group = QGroupBox("Application")
        self.app_group.setStyleSheet(self.theme_group.styleSheet())
        app_layout = QFormLayout(self.app_group)
        
        # Placeholder for future settings
        self.placeholder_label = QLabel("More settings coming soon...")
        self.placeholder_label.setStyleSheet("color: #c3c3c3; font-style: italic; font-size: 14px;")
        app_layout.addWidget(self.placeholder_label)
        
        scroll_layout.addWidget(self.app_group)
        
        # Add stretch to push everything to the top
        scroll_layout.addStretch()
        
        # Setup scroll area
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        main_layout.addWidget(self.scroll_area)
        
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
    
    def apply_theme(self, theme: dict):
        """Apply theme colors to the settings page"""
        self.current_theme = theme
        
        # Apply to scroll widget background
        self.scroll_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {theme['main_bg']};
            }}
        """)
        
        # Apply to title
        self.title.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {theme['text_primary']};
            margin-bottom: 20px;
            background-color: transparent;
        """)
        
        # Apply to group boxes
        group_style = f"""
            QGroupBox {{
                font-size: 16px;
                font-weight: bold;
                color: {theme['text_primary']};
                border: 2px solid {theme['input_border']};
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 10px;
                background-color: transparent;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
        """
        self.theme_group.setStyleSheet(group_style)
        self.app_group.setStyleSheet(group_style)
        
        # Apply to theme combo box
        self.theme_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {theme['input_bg']};
                border: 1px solid {theme['input_border']};
                padding: 8px 12px;
                border-radius: 4px;
                color: {theme['text_primary']};
                font-size: 14px;
                min-width: 200px;
            }}
            QComboBox:hover {{
                border-color: {theme['button_bg']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {theme['text_secondary']};
                margin-right: 5px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {theme['input_bg']};
                border: 1px solid {theme['input_border']};
                selection-background-color: {theme['button_bg']};
                color: {theme['text_primary']};
            }}
        """)
        
        # Apply to labels
        self.theme_label.setStyleSheet(f"""
            color: {theme['text_secondary']};
            font-size: 14px;
            background-color: transparent;
        """)
        self.placeholder_label.setStyleSheet(f"""
            color: {theme['text_secondary']};
            font-style: italic;
            font-size: 14px;
            background-color: transparent;
        """)
        
        # Apply to scroll area
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {theme['main_bg']};
            }}
        """)

