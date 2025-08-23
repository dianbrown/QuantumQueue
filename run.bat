@echo off
echo ================================================
echo CPU Scheduling Practice Application
echo ================================================
echo.
echo Starting the application...
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please run "setup.bat" first to install dependencies.
    pause
    exit /b 1
)

echo Checking for PySide6...
python -c "import PySide6" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: PySide6 is not installed!
    echo Please run "setup.bat" first to install dependencies.
    pause
    exit /b 1
)

echo Launching CPU Scheduling App...
python main_new.py

if %errorlevel% neq 0 (
    echo.
    echo The application encountered an error.
    echo Press any key to exit...
    pause >nul
)
