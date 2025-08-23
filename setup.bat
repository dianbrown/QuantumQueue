@echo off
echo ================================================
echo CPU Scheduling App - Setup Script
echo ================================================
echo.
echo This script will install the required dependencies.
echo Please make sure you have Python installed on your system.
echo.
pause

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
echo.

echo Installing PySide6 (Qt for Python)...
pip install PySide6

if %errorlevel% neq 0 (
    echo ERROR: Failed to install PySide6!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo ================================================
echo Setup completed successfully!
echo ================================================
echo.
echo You can now run the application by:
echo 1. Double-clicking "run.bat"
echo 2. Or running "python main.py" in terminal
echo.
echo Press any key to exit...
pause >nul
