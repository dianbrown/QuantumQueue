# CPU Scheduling Practice Application

Tired trying to get practice examples or solutions for the CPU Scheduling problems?? Well look no further, this application aims to make studying easier and to instantly get the solution to a problem.

No more making tedious excell spread sheets or worse... drawing everything by HAND!!

just enter everything into the application, it has a built in random function and value editor for ease of use

The TAT and WT are also calculated when you view the solution as well as the responsiveness per process.
Feel free to enter your own values to view solutions or just practice the algorithms with the randomize function.

## 🚀 Quick Start (Easy Installation)

### For Windows Users (Double-Click Setup):
1. **Download** the project as ZIP from GitHub
2. **Extract** the ZIP file to any folder
3. **Double-click** `setup.bat` to install dependencies automatically
4. **Double-click** `run.bat` to start the application
5. **Done!** 🎉

### For All Platforms:
1. **Download** and extract the project
2. **Double-click** `setup.py` (or run `python setup.py`)
3. **Run** `python main.py` to start the application

### Manual Installation:
```bash
# Install Python 3.8+ from python.org
pip install PySide6
python main.py
```

## Project Structure

```
CPU_SchedulingPython/
├── setup.bat               # 🖱️ Windows setup (double-click)
├── run.bat                 # 🖱️ Windows launcher (double-click)
├── setup.py                # 🖱️ Cross-platform setup (double-click)
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── models/                 # Data models
│   ├── __init__.py
│   ├── process.py         # Process data class
│   └── scheduling_result.py # Result data class
├── algorithms/             # Scheduling algorithms
│   ├── __init__.py
│   ├── base_scheduler.py  # Abstract base class
│   ├── fcfs.py           # First Come First Served
│   ├── fcfs_priority.py  # FCFS with Priority
│   ├── round_robin.py    # Round Robin
│   ├── sjf.py           # Shortest Job First 
│   ├── sjf_priority.py  # Shortest Job First Priority
│   └── srt.py           # Shortest Remaining Time (template)
├── ui/                    # User interface components
│   ├── __init__.py
│   └── main_window.py    # Main application window
└── utils/                 # Utility functions
    ├── __init__.py
    └── process_generator.py # Random process generator
```

## Features

### Current Implementation
- ✅ **FCFS (First Come First Served)**: Non-preemptive scheduling
- ✅ **FCFS with Priority**: Preemptive priority scheduling
- ✅ **Smart Process Generation**: Eliminates gaps for better visualization
- ✅ **Interactive Timeline**: Click and double-click to fill cells
- ✅ **Solution Checking**: Compare your input with the correct solution
- ✅ **Metrics Display**: Waiting time, turnaround time, averages
- ✅ **Easy Installation**: Double-click setup for Windows users
- ✅ **Round Robin (RR)**: Time quantum-based scheduling
- ✅ **Round Robin with Priority (RRP)**: Priority + time quantum
- ✅ **Shortest Job First (SJF)**: Non-preemptive shortest job
- ✅ **SJF with Priority (SJFP)**: Priority + shortest job
- ✅ **Shortest Remaining Time (SRT)**: Preemptive shortest remaining time
- ✅ **Responsiveness per process**: Calculates the responsiveness and displays it

## 📖 How to Use the Application

### 🎯 Practice Mode:
1. **Select Algorithm**: Choose FCFS or FCFS with Priority from dropdown
2. **Generate Processes**: Click "Randomize" for new practice problems
3. **Fill Timeline**: Click cells to schedule processes manually
   - **Single click**: Fill one time slot
   - **Double click**: Auto-fill entire burst time
   - **Right-Click**: Adds RS (Ready State) Markers
4. **Check Solution**: Click "Check Solution" to see if you're correct
5. **Show Answer**: Click "Show Solution" to see the correct schedule
6. **Reset**: Click "Reset" to clear and try again

### ⚙️ Advanced Features:
- **Add/Delete Processes**: Modify the process list manually
- **Edit Process Data**: Change arrival times, burst times, priorities
- **Reset**: Generate fresh timeline after editing processes
- **Metrics Display**: View waiting times, turnaround times, and averages
