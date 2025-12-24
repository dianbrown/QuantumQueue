"""
Settings Page for theme selection and other application preferences
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox,
                              QGroupBox, QFormLayout, QScrollArea, QCheckBox,
                              QPushButton, QHBoxLayout, QFileDialog, QMessageBox)
from PySide6.QtCore import Signal, QSettings
from PySide6.QtGui import QFontDatabase, QFont
from themes.theme_manager import ThemeManager
import json
import os


# Colorblind-safe color palettes for PRA hit/fault indicators
COLORBLIND_PALETTES = {
    "Default": {
        "hit_color": "#4caf50",      # Green
        "fault_color": "#f44336",    # Red
        "description": "Standard green/red colors"
    },
    "Deuteranopia": {
        "hit_color": "#2196f3",      # Blue
        "fault_color": "#ff9800",    # Orange
        "description": "Blue/Orange - safe for red-green color blindness"
    },
    "Protanopia": {
        "hit_color": "#00bcd4",      # Cyan
        "fault_color": "#e91e63",    # Magenta
        "description": "Cyan/Magenta - safe for red color blindness"
    },
    "High Contrast": {
        "hit_color": "#000000",      # Black
        "fault_color": "#ffeb3b",    # Yellow
        "description": "Maximum contrast for visibility"
    }
}

# Font size scaling options
FONT_SCALES = {
    "Small (90%)": 0.9,
    "Normal (100%)": 1.0,
    "Large (110%)": 1.1,
    "Extra Large (120%)": 1.2
}

# Font family options
FONT_FAMILIES = {
    "System Default": "",
    "OpenDyslexic": "OpenDyslexic"
}

# Startup page options
STARTUP_PAGES = {
    "Home": 0,
    "CPU Scheduling": 1,
    "Page Replacement": 2,
    "Help": 3,
    "Settings": 4
}


class SettingsPage(QWidget):
    """Settings page with theme selection and other preferences"""
    
    theme_changed = Signal(str)  # Signal emitted when theme changes
    colorblind_mode_changed = Signal(str, str)  # hit_color, fault_color
    font_scale_changed = Signal(float)  # Scale factor
    font_family_changed = Signal(str)  # Font family name
    startup_page_changed = Signal(int)  # Page index
    
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
        scroll_layout.setSpacing(20)
        
        # Title
        self.title = QLabel("Settings")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff; margin-bottom: 20px;")
        scroll_layout.addWidget(self.title)
        
        # Theme settings group
        self.theme_group = self.create_appearance_group()
        scroll_layout.addWidget(self.theme_group)
        
        # Accessibility settings group
        self.accessibility_group = self.create_accessibility_group()
        scroll_layout.addWidget(self.accessibility_group)
        
        # Window behavior settings group
        self.window_group = self.create_window_behavior_group()
        scroll_layout.addWidget(self.window_group)
        
        # Data management group
        self.data_group = self.create_data_management_group()
        scroll_layout.addWidget(self.data_group)
        
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
    
    def get_group_style(self):
        """Get the common style for group boxes"""
        return """
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
        """
    
    def get_combo_style(self):
        """Get the common style for combo boxes"""
        return """
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
        """
    
    def get_checkbox_style(self):
        """Get the common style for checkboxes"""
        return """
            QCheckBox {
                color: #c3c3c3;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #72767d;
                border-radius: 4px;
                background-color: #40444b;
            }
            QCheckBox::indicator:checked {
                background-color: #7289da;
                border-color: #7289da;
            }
            QCheckBox::indicator:hover {
                border-color: #7289da;
            }
        """
    
    def get_button_style(self):
        """Get the common style for buttons"""
        return """
            QPushButton {
                background-color: #7289da;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                font-size: 13px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #677bc4;
            }
            QPushButton:pressed {
                background-color: #5b6eae;
            }
        """
    
    def create_appearance_group(self):
        """Create the appearance settings group"""
        group = QGroupBox("Appearance")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout(group)
        layout.setSpacing(15)
        
        # Theme selection
        self.theme_combo = QComboBox()
        available_themes = self.theme_manager.get_available_themes()
        if available_themes:
            self.theme_combo.addItems(available_themes)
        else:
            self.theme_combo.addItems(["Dracula"])
        self.theme_combo.setStyleSheet(self.get_combo_style())
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        
        self.theme_label = QLabel("Theme:")
        self.theme_label.setStyleSheet("color: #c3c3c3; font-size: 14px;")
        layout.addRow(self.theme_label, self.theme_combo)
        
        return group
    
    def create_accessibility_group(self):
        """Create the accessibility settings group"""
        group = QGroupBox("Accessibility")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout(group)
        layout.setSpacing(15)
        
        # Colorblind mode selection
        self.colorblind_combo = QComboBox()
        self.colorblind_combo.addItems(list(COLORBLIND_PALETTES.keys()))
        self.colorblind_combo.setStyleSheet(self.get_combo_style())
        self.colorblind_combo.currentTextChanged.connect(self.on_colorblind_mode_changed)
        
        self.colorblind_label = QLabel("Colorblind Mode:")
        self.colorblind_label.setStyleSheet("color: #c3c3c3; font-size: 14px;")
        layout.addRow(self.colorblind_label, self.colorblind_combo)
        
        # Color preview
        self.color_preview_widget = QWidget()
        preview_layout = QHBoxLayout(self.color_preview_widget)
        preview_layout.setContentsMargins(0, 5, 0, 5)
        preview_layout.setSpacing(10)
        
        self.hit_preview = QLabel("  Hit  ")
        self.hit_preview.setStyleSheet("""
            background-color: #4caf50;
            color: white;
            padding: 5px 15px;
            border-radius: 4px;
            font-weight: bold;
        """)
        
        self.fault_preview = QLabel("  Fault  ")
        self.fault_preview.setStyleSheet("""
            background-color: #f44336;
            color: white;
            padding: 5px 15px;
            border-radius: 4px;
            font-weight: bold;
        """)
        
        preview_layout.addWidget(self.hit_preview)
        preview_layout.addWidget(self.fault_preview)
        preview_layout.addStretch()
        
        self.preview_label = QLabel("Color Preview:")
        self.preview_label.setStyleSheet("color: #c3c3c3; font-size: 14px;")
        layout.addRow(self.preview_label, self.color_preview_widget)
        
        # Colorblind mode description
        self.colorblind_desc = QLabel(COLORBLIND_PALETTES["Default"]["description"])
        self.colorblind_desc.setStyleSheet("color: #888; font-size: 12px; font-style: italic;")
        self.colorblind_desc.setWordWrap(True)
        layout.addRow("", self.colorblind_desc)
        
        # Font size selection
        self.font_scale_combo = QComboBox()
        self.font_scale_combo.addItems(list(FONT_SCALES.keys()))
        self.font_scale_combo.setStyleSheet(self.get_combo_style())
        self.font_scale_combo.currentTextChanged.connect(self.on_font_scale_changed)
        
        self.font_scale_label = QLabel("Font Size:")
        self.font_scale_label.setStyleSheet("color: #c3c3c3; font-size: 14px;")
        layout.addRow(self.font_scale_label, self.font_scale_combo)
        
        # Font family selection (for dyslexia support)
        self.font_family_combo = QComboBox()
        self.font_family_combo.addItems(list(FONT_FAMILIES.keys()))
        self.font_family_combo.setStyleSheet(self.get_combo_style())
        self.font_family_combo.currentTextChanged.connect(self.on_font_family_changed)
        
        self.font_family_label = QLabel("Font (Dyslexia Support):")
        self.font_family_label.setStyleSheet("color: #c3c3c3; font-size: 14px;")
        layout.addRow(self.font_family_label, self.font_family_combo)
        
        # Font family description
        self.font_family_desc = QLabel("OpenDyslexic is a font designed to help readers with dyslexia")
        self.font_family_desc.setStyleSheet("color: #888; font-size: 12px; font-style: italic;")
        self.font_family_desc.setWordWrap(True)
        layout.addRow("", self.font_family_desc)
        
        return group
    
    def create_window_behavior_group(self):
        """Create the window behavior settings group"""
        group = QGroupBox("Window Behavior")
        group.setStyleSheet(self.get_group_style())
        
        layout = QVBoxLayout(group)
        layout.setSpacing(12)
        
        # Remember window position checkbox
        self.remember_position_cb = QCheckBox("Remember window position and size")
        self.remember_position_cb.setStyleSheet(self.get_checkbox_style())
        self.remember_position_cb.stateChanged.connect(self.on_remember_position_changed)
        layout.addWidget(self.remember_position_cb)
        
        # Start maximized checkbox
        self.start_maximized_cb = QCheckBox("Start maximized")
        self.start_maximized_cb.setStyleSheet(self.get_checkbox_style())
        self.start_maximized_cb.stateChanged.connect(self.on_start_maximized_changed)
        layout.addWidget(self.start_maximized_cb)
        
        # Startup page selection
        startup_layout = QHBoxLayout()
        startup_layout.setSpacing(10)
        
        self.startup_page_label = QLabel("Startup page:")
        self.startup_page_label.setStyleSheet("color: #c3c3c3; font-size: 14px;")
        
        self.startup_page_combo = QComboBox()
        self.startup_page_combo.addItems(list(STARTUP_PAGES.keys()))
        self.startup_page_combo.setStyleSheet(self.get_combo_style())
        self.startup_page_combo.currentTextChanged.connect(self.on_startup_page_changed)
        
        startup_layout.addWidget(self.startup_page_label)
        startup_layout.addWidget(self.startup_page_combo)
        startup_layout.addStretch()
        layout.addLayout(startup_layout)
        
        return group
    
    def create_data_management_group(self):
        """Create the data management settings group"""
        group = QGroupBox("Data Management")
        group.setStyleSheet(self.get_group_style())
        
        layout = QVBoxLayout(group)
        layout.setSpacing(15)
        
        # Description
        desc_label = QLabel("Export, import, or reset your application settings.")
        desc_label.setStyleSheet("color: #c3c3c3; font-size: 14px;")
        layout.addWidget(desc_label)
        
        # Buttons row
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.export_btn = QPushButton("Export Settings")
        self.export_btn.setStyleSheet(self.get_button_style())
        self.export_btn.clicked.connect(self.export_settings)
        
        self.import_btn = QPushButton("Import Settings")
        self.import_btn.setStyleSheet(self.get_button_style())
        self.import_btn.clicked.connect(self.import_settings)
        
        self.reset_btn = QPushButton("Reset All")
        self.reset_btn.setStyleSheet(self.get_button_style().replace("#7289da", "#f44336").replace("#677bc4", "#d32f2f").replace("#5b6eae", "#c62828"))
        self.reset_btn.clicked.connect(self.reset_all_settings)
        
        buttons_layout.addWidget(self.export_btn)
        buttons_layout.addWidget(self.import_btn)
        buttons_layout.addWidget(self.reset_btn)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        return group
        
    def on_theme_changed(self, theme_name):
        """Handle theme change"""
        self.settings.setValue("theme", theme_name)
        self.theme_changed.emit(theme_name)
    
    def on_colorblind_mode_changed(self, mode_name):
        """Handle colorblind mode change"""
        self.settings.setValue("colorblind_mode", mode_name)
        palette = COLORBLIND_PALETTES.get(mode_name, COLORBLIND_PALETTES["Default"])
        
        # Update color preview
        self.hit_preview.setStyleSheet(f"""
            background-color: {palette['hit_color']};
            color: white;
            padding: 5px 15px;
            border-radius: 4px;
            font-weight: bold;
        """)
        self.fault_preview.setStyleSheet(f"""
            background-color: {palette['fault_color']};
            color: white;
            padding: 5px 15px;
            border-radius: 4px;
            font-weight: bold;
        """)
        
        # Update description
        self.colorblind_desc.setText(palette["description"])
        
        # Emit signal with colors
        self.colorblind_mode_changed.emit(palette['hit_color'], palette['fault_color'])
    
    def on_font_scale_changed(self, scale_name):
        """Handle font scale change"""
        self.settings.setValue("font_scale", scale_name)
        scale_value = FONT_SCALES.get(scale_name, 1.0)
        self.font_scale_changed.emit(scale_value)
    
    def on_font_family_changed(self, family_name):
        """Handle font family change"""
        self.settings.setValue("font_family", family_name)
        font_family = FONT_FAMILIES.get(family_name, "")
        self.font_family_changed.emit(font_family)
    
    def on_remember_position_changed(self, state):
        """Handle remember position checkbox change"""
        self.settings.setValue("remember_position", state == 2)  # Qt.Checked = 2
    
    def on_start_maximized_changed(self, state):
        """Handle start maximized checkbox change"""
        self.settings.setValue("start_maximized", state == 2)
    
    def on_startup_page_changed(self, page_name):
        """Handle startup page change"""
        self.settings.setValue("startup_page", page_name)
        page_index = STARTUP_PAGES.get(page_name, 0)
        self.startup_page_changed.emit(page_index)
    
    def export_settings(self):
        """Export all settings to a JSON file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Settings", "quantumqueue_settings.json",
            "JSON Files (*.json)"
        )
        
        if file_path:
            settings_data = {
                "theme": self.theme_combo.currentText(),
                "colorblind_mode": self.colorblind_combo.currentText(),
                "font_scale": self.font_scale_combo.currentText(),
                "remember_position": self.remember_position_cb.isChecked(),
                "start_maximized": self.start_maximized_cb.isChecked(),
                "startup_page": self.startup_page_combo.currentText()
            }
            
            try:
                with open(file_path, 'w') as f:
                    json.dump(settings_data, f, indent=4)
                QMessageBox.information(self, "Success", "Settings exported successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to export settings: {e}")
    
    def import_settings(self):
        """Import settings from a JSON file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Settings", "",
            "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    settings_data = json.load(f)
                
                # Apply imported settings
                if "theme" in settings_data:
                    index = self.theme_combo.findText(settings_data["theme"])
                    if index >= 0:
                        self.theme_combo.setCurrentIndex(index)
                
                if "colorblind_mode" in settings_data:
                    index = self.colorblind_combo.findText(settings_data["colorblind_mode"])
                    if index >= 0:
                        self.colorblind_combo.setCurrentIndex(index)
                
                if "font_scale" in settings_data:
                    index = self.font_scale_combo.findText(settings_data["font_scale"])
                    if index >= 0:
                        self.font_scale_combo.setCurrentIndex(index)
                
                if "remember_position" in settings_data:
                    self.remember_position_cb.setChecked(settings_data["remember_position"])
                
                if "start_maximized" in settings_data:
                    self.start_maximized_cb.setChecked(settings_data["start_maximized"])
                
                if "startup_page" in settings_data:
                    index = self.startup_page_combo.findText(settings_data["startup_page"])
                    if index >= 0:
                        self.startup_page_combo.setCurrentIndex(index)
                
                QMessageBox.information(self, "Success", "Settings imported successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to import settings: {e}")
    
    def reset_all_settings(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(
            self, "Reset Settings",
            "Are you sure you want to reset all settings to their defaults?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Reset to defaults
            self.theme_combo.setCurrentText("Dracula")
            self.colorblind_combo.setCurrentText("Default")
            self.font_scale_combo.setCurrentText("Normal (100%)")
            self.remember_position_cb.setChecked(False)
            self.start_maximized_cb.setChecked(False)
            self.startup_page_combo.setCurrentText("Home")
            
            # Clear stored settings
            self.settings.clear()
            
            QMessageBox.information(self, "Success", "All settings have been reset to defaults.")
        
    def load_settings(self):
        """Load saved settings"""
        # Theme
        saved_theme = self.settings.value("theme", "Dracula")
        if saved_theme:
            index = self.theme_combo.findText(saved_theme)
            if index >= 0:
                self.theme_combo.setCurrentIndex(index)
        
        # Colorblind mode
        saved_colorblind = self.settings.value("colorblind_mode", "Default")
        if saved_colorblind:
            index = self.colorblind_combo.findText(saved_colorblind)
            if index >= 0:
                self.colorblind_combo.setCurrentIndex(index)
                # Update preview colors
                self.on_colorblind_mode_changed(saved_colorblind)
        
        # Font scale
        saved_font_scale = self.settings.value("font_scale", "Normal (100%)")
        if saved_font_scale:
            index = self.font_scale_combo.findText(saved_font_scale)
            if index >= 0:
                self.font_scale_combo.setCurrentIndex(index)
        
        # Font family
        saved_font_family = self.settings.value("font_family", "System Default")
        if saved_font_family:
            index = self.font_family_combo.findText(saved_font_family)
            if index >= 0:
                self.font_family_combo.setCurrentIndex(index)
        
        # Window behavior
        self.remember_position_cb.setChecked(
            self.settings.value("remember_position", False, type=bool)
        )
        self.start_maximized_cb.setChecked(
            self.settings.value("start_maximized", False, type=bool)
        )
        
        # Startup page
        saved_startup = self.settings.value("startup_page", "Home")
        if saved_startup:
            index = self.startup_page_combo.findText(saved_startup)
            if index >= 0:
                self.startup_page_combo.setCurrentIndex(index)
    
    def get_colorblind_colors(self):
        """Get current hit/fault colors based on colorblind mode"""
        mode = self.colorblind_combo.currentText()
        palette = COLORBLIND_PALETTES.get(mode, COLORBLIND_PALETTES["Default"])
        return palette['hit_color'], palette['fault_color']
    
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
        self.accessibility_group.setStyleSheet(group_style)
        self.window_group.setStyleSheet(group_style)
        self.data_group.setStyleSheet(group_style)
        
        # Apply to combo boxes
        combo_style = f"""
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
        """
        self.theme_combo.setStyleSheet(combo_style)
        self.colorblind_combo.setStyleSheet(combo_style)
        self.font_scale_combo.setStyleSheet(combo_style)
        self.font_family_combo.setStyleSheet(combo_style)
        self.startup_page_combo.setStyleSheet(combo_style)
        
        # Apply to checkboxes
        checkbox_style = f"""
            QCheckBox {{
                color: {theme['text_secondary']};
                font-size: 14px;
                spacing: 8px;
                background-color: transparent;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {theme['input_border']};
                border-radius: 4px;
                background-color: {theme['input_bg']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {theme['button_bg']};
                border-color: {theme['button_bg']};
            }}
            QCheckBox::indicator:hover {{
                border-color: {theme['button_bg']};
            }}
        """
        self.remember_position_cb.setStyleSheet(checkbox_style)
        self.start_maximized_cb.setStyleSheet(checkbox_style)
        
        # Apply to buttons
        button_style = f"""
            QPushButton {{
                background-color: {theme['button_bg']};
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                color: {theme.get('button_text', theme['text_primary'])};
                font-weight: bold;
                font-size: 13px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {theme['button_hover']};
            }}
        """
        self.export_btn.setStyleSheet(button_style)
        self.import_btn.setStyleSheet(button_style)
        
        # Reset button stays red
        self.reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #f44336;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                font-size: 13px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: #d32f2f;
            }}
        """)
        
        # Apply to labels
        label_style = f"""
            color: {theme['text_secondary']};
            font-size: 14px;
            background-color: transparent;
        """
        self.theme_label.setStyleSheet(label_style)
        self.colorblind_label.setStyleSheet(label_style)
        self.font_scale_label.setStyleSheet(label_style)
        self.preview_label.setStyleSheet(label_style)
        self.startup_page_label.setStyleSheet(label_style)
        
        # Colorblind description
        self.colorblind_desc.setStyleSheet(f"""
            color: {theme['text_secondary']};
            font-size: 12px;
            font-style: italic;
            background-color: transparent;
        """)
        
        # Apply to scroll area
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {theme['main_bg']};
            }}
        """)
