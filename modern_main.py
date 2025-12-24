"""
Modern GUI Main Window with Sidebar Menu
Inspired by PyDracula design
"""

import sys
import os
from PySide6.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, QFrame, QStackedWidget,
                              QLabel, QSizePolicy, QComboBox)
from PySide6.QtCore import Qt, QRect, QSize, Signal, QSettings
from PySide6.QtGui import QIcon, QPixmap, QColor

# Import resource path helper
from resource_path import resource_path

# Import the existing CPU scheduling app
from CPU.ui.main_window import CPUSchedulingApp
# Import the PRA app
from PRA.ui.main_window import PRAMainWindow
# Import the theme manager
from themes.theme_manager import ThemeManager

# Import custom UI components from pages directory
from pages.CustomTitleBar import CustomTitleBar
from pages.Sidebar import CollapsibleSidebar
from pages.HelpPage import HelpPage
from pages.SettingsPage import SettingsPage


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
        self.startup_page_index = 1  # Default to Home
        self._first_show = True  # Track first show event
        
        # Initialize settings and theme manager
        self.settings = QSettings()
        self.theme_manager = ThemeManager()
        
        self.setup_ui()
        
        # Apply saved theme or default
        saved_theme = self.settings.value("theme", "Dracula")
        self.apply_theme(saved_theme)
        
        # Restore window geometry if setting is enabled
        if self.settings.value("remember_position", False, type=bool):
            geometry = self.settings.value("window_geometry")
            if geometry:
                self.restoreGeometry(geometry)
        
        # Check if should start maximized
        if self.settings.value("start_maximized", False, type=bool):
            self.showMaximized()
    
    def showEvent(self, event):
        """Handle show event to ensure sidebar is on top and apply startup settings"""
        super().showEvent(event)
        if hasattr(self, 'sidebar'):
            self.sidebar.raise_()
        
        # Apply startup page on first show
        if self._first_show:
            self._first_show = False
            startup_page = self.settings.value("startup_page", "Home")
            # Map page names to indices
            page_map = {"Home": 1, "CPU Scheduling": 2, "Page Replacement": 3, "Help": 4, "Settings": 5}
            page_index = page_map.get(startup_page, 1)
            self.change_page(page_index)
    
    def closeEvent(self, event):
        """Handle close event to save window geometry"""
        if self.settings.value("remember_position", False, type=bool):
            self.settings.setValue("window_geometry", self.saveGeometry())
        super().closeEvent(event)
    
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
        self.sidebar = CollapsibleSidebar(self)  # Pass self as parent
        self.sidebar.menu_changed.connect(self.change_page)
        # Move sidebar to be on top of everything
        self.sidebar.raise_()
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
        self.settings_page.colorblind_mode_changed.connect(self.apply_colorblind_mode)
        self.settings_page.font_family_changed.connect(self.apply_font_family)
        self.settings_page.font_scale_changed.connect(self.apply_font_scale)
        self.settings_page.startup_page_changed.connect(self.set_startup_page)
        self.content_stack.addWidget(self.settings_page)
        
        # Apply saved colorblind mode to PRA page and tutorials
        hit_color, fault_color = self.settings_page.get_colorblind_colors()
        self.pra_page.set_hit_fault_colors(hit_color, fault_color)
        # Also apply to help page tutorials
        if hasattr(self.help_page, 'set_hit_fault_colors'):
            self.help_page.set_hit_fault_colors(hit_color, fault_color)
    
    def create_home_page(self):
        """Create the home page with logo and application information"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Logo
        logo_label = QLabel()
        logo_path = resource_path("Assets/Icons/QuantumQueue2.png")
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
        # Ensure sidebar stays on top after page change
        self.sidebar.raise_()
    
    def apply_colorblind_mode(self, hit_color: str, fault_color: str):
        """Apply colorblind mode colors to PRA page and all PRA tutorials"""
        # Apply to main PRA page and force refresh
        self.pra_page.set_hit_fault_colors(hit_color, fault_color)
        
        # Apply to all PRA tutorial pages in Help page
        if hasattr(self.help_page, 'set_hit_fault_colors'):
            self.help_page.set_hit_fault_colors(hit_color, fault_color)
    
    def apply_font_family(self, font_family: str):
        """Apply font family throughout the application"""
        from PySide6.QtWidgets import QApplication
        from PySide6.QtGui import QFont, QFontDatabase
        from resource_path import resource_path
        import os
        
        app = QApplication.instance()
        if not app:
            return
        
        current_font = app.font()
        current_size = current_font.pointSize()
        
        if font_family and font_family != "":
            # Try to load OpenDyslexic font from bundled file
            if "OpenDyslexic" in font_family:
                # Try multiple font file locations
                font_paths = [
                    resource_path("Assets/fonts/OpenDyslexic-Regular.otf"),
                    resource_path("Assets/fonts/OpenDyslexic-Regular.ttf"),
                    "Assets/fonts/OpenDyslexic-Regular.otf",
                    "Assets/fonts/OpenDyslexic-Regular.ttf",
                ]
                
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        font_id = QFontDatabase.addApplicationFont(font_path)
                        if font_id >= 0:
                            families = QFontDatabase.applicationFontFamilies(font_id)
                            if families:
                                font_family = families[0]
                        break
            
            # Apply the font
            new_font = QFont(font_family)
            new_font.setPointSize(current_size)
            app.setFont(new_font)
        else:
            # Reset to system default - use "Segoe UI" on Windows, system font on others
            import sys
            if sys.platform == "win32":
                default_family = "Segoe UI"
            else:
                default_family = QFontDatabase.systemFont(QFontDatabase.GeneralFont).family()
            
            default_font = QFont(default_family)
            default_font.setPointSize(current_size)
            app.setFont(default_font)
        
        # Force all widgets to update with new font
        self._refresh_all_widget_styles()
    
    def apply_font_scale(self, scale: float):
        """Apply font scale throughout the application"""
        from PySide6.QtWidgets import QApplication
        from PySide6.QtGui import QFont
        
        app = QApplication.instance()
        if not app:
            return
        
        # Base font size is typically 9-10 points
        base_size = 10
        new_size = max(8, int(base_size * scale))  # Minimum of 8pt
        current_font = app.font()
        current_font.setPointSize(new_size)
        app.setFont(current_font)
        
        # Force all widgets to update with new font
        self._refresh_all_widget_styles()
    
    def _refresh_all_widget_styles(self):
        """Force refresh of all widget styles to apply font changes"""
        from PySide6.QtWidgets import QApplication
        
        app = QApplication.instance()
        if app:
            # Process all widgets recursively
            for widget in app.allWidgets():
                try:
                    # Update font from application
                    widget.setFont(app.font())
                    # Force style recalculation
                    if widget.style():
                        widget.style().unpolish(widget)
                        widget.style().polish(widget)
                    widget.update()
                except (RuntimeError, TypeError):
                    # Skip widgets that can't be updated (deleted or special widgets)
                    pass
    
    def set_startup_page(self, page_index: int):
        """Set the startup page preference (saved for next launch)"""
        # This is handled by QSettings in SettingsPage, just store for reference
        self.startup_page_index = page_index
        
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
                color: {theme.get('button_text', theme['text_primary'])};
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
                color: {theme.get('button_text', theme['text_primary'])};
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
        
        # Apply Settings page theme
        if hasattr(self.settings_page, 'apply_theme'):
            self.settings_page.apply_theme(theme)
        
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
