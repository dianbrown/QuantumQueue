"""
CPU Scheduling & Page Replacement Practice Application

A modern Qt-based application for practicing CPU scheduling algorithms and Page Replacement Algorithms.
Features a collapsible sidebar menu with sections for CPU Scheduling, PRA, and Settings.
"""

import sys
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
