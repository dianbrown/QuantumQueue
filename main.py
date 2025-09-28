"""
CPU Scheduling Practice Application

A Qt-based application for practicing CPU scheduling algorithms.
Supports FCFS, FCFS with Priority, and future algorithms like RR, SJF, etc.
"""

import sys
from PySide6.QtWidgets import QApplication
from CPU.ui.main_window import CPUSchedulingApp


def main():
    """Main entry point for the CPU Scheduling application."""
    app = QApplication(sys.argv)
    window = CPUSchedulingApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
