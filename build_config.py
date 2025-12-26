"""
Build configuration for creating installers
Uses PyInstaller to create executables and installers
"""

import os
import sys
import platform

# Application metadata
APP_NAME = "QuantumQueue"
APP_VERSION = "2.0.0"
APP_AUTHOR = "dianbrown"
APP_DESCRIPTION = "CPU Scheduling & Page Replacement Practice Application"
APP_URL = "https://github.com/dianbrown/QuantumQueue"

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(ROOT_DIR, "Assets", "Icons", "QuantumQueue2.png")
ICON_ICO = os.path.join(ROOT_DIR, "Assets", "Icons", "app_icon.ico")
ICON_ICNS = os.path.join(ROOT_DIR, "Assets", "Icons", "app_icon.icns")

# PyInstaller build options
PYINSTALLER_OPTIONS = {
    'name': APP_NAME,
    'onefile': False,  # Use onedir for better performance
    'windowed': True,  # No console window
    'icon': ICON_ICO if platform.system() == 'Windows' else ICON_ICNS,
    'add_data': [
        ('themes', 'themes'),
        ('Assets', 'Assets'),
    ('tutorial_kb', 'tutorial_kb'),
    ],
    'hidden_imports': [
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'CPU.algorithms',
        'CPU.models',
        'CPU.ui',
        'CPU.utils',
        'PRA.algorithms',
        'PRA.models',
        'PRA.ui',
        'pages',
        'themes.theme_manager',
    ],
    'exclude_modules': [
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
    ],
}

# Platform-specific configurations
if platform.system() == 'Windows':
    INSTALLER_TYPE = 'NSIS'  # Nullsoft Scriptable Install System
elif platform.system() == 'Darwin':
    INSTALLER_TYPE = 'DMG'
else:
    INSTALLER_TYPE = 'AppImage'
