"""
CPU Scheduling & Page Replacement Practice Application

A modern Qt-based application for practicing CPU scheduling algorithms and Page Replacement Algorithms.
Features a collapsible sidebar menu with sections for CPU Scheduling, PRA, and Settings.
"""

import sys
import os

# Suppress Qt debug warnings about QPainter (harmless rendering timing issues)
os.environ["QT_LOGGING_RULES"] = "qt.qpa.paint=false"

# Redirect Qt warnings to suppress QPainter messages
from PySide6.QtCore import qInstallMessageHandler, QtMsgType

def qt_message_handler(mode, context, message):
    """Suppress Qt QPainter warnings which are harmless."""
    if "QPainter" in message or "Painter not active" in message:
        return  # Ignore these warnings
    # Print other messages normally
    if mode == QtMsgType.QtWarningMsg:
        print(f"Qt Warning: {message}")
    elif mode == QtMsgType.QtCriticalMsg:
        print(f"Qt Critical: {message}")
    elif mode == QtMsgType.QtFatalMsg:
        print(f"Qt Fatal: {message}")

qInstallMessageHandler(qt_message_handler)

from modern_main import main as modern_main


def main():
    """Main entry point for the modern GUI application."""
    try:
        modern_main()
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
