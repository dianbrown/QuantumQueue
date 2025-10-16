# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for QuantumQueue
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all data files
datas = [
    ('themes', 'themes'),
    ('Assets', 'Assets'),
]

# Collect all hidden imports
hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'PySide6.QtSvg',
]

# Add all submodules
hiddenimports += collect_submodules('CPU')
hiddenimports += collect_submodules('PRA')
hiddenimports += collect_submodules('pages')
hiddenimports += collect_submodules('themes')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'scipy', 'pandas'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='QuantumQueue',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Assets/Icons/app_icon.ico' if sys.platform == 'win32' else 'Assets/Icons/app_icon.icns',
)

# Note: This creates a single-file executable
# Windows: dist/QuantumQueue.exe
# macOS: For .app bundle, use onedir mode instead
