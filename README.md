# QuantumQueue - CPU Scheduling & Page Replacement Practice

<p align="center">
  <img src="Assets/Icons/QuantumQueue2.png" alt="QuantumQueue Logo" width="200"/>
</p>

<p align="center">
  <strong>Interactive learning tool for CPU Scheduling and Page Replacement Algorithms</strong>
</p>

just enter everything into the application, it has a built in random function and value editor for ease of use

The TAT and WT are also calculated when you view the solution as well as the responsiveness per process.
Feel free to enter your own values to view solutions or just practice the algorithms with the randomize function.

---

## 📥 Quick Start

### 🎯 Easy Installation (Recommended)

#### Windows Users:
1. **Download** the installer from [Releases](https://github.com/dianbrown/CPU-SchedulingApp/releases/latest)
2. **Run** `QuantumQueue-*-Windows-Setup.exe`
3. **Follow** the installation wizard
4. **Launch** from Desktop shortcut or Start Menu
5. **Done!** 🎉

#### macOS Users:
1. **Download** the DMG from [Releases](https://github.com/dianbrown/CPU-SchedulingApp/releases/latest)
2. **Open** `QuantumQueue-*-macOS.dmg`
3. **Drag** QuantumQueue to Applications folder
4. **Launch** from Applications
5. **Done!** 🎉

### 🛠️ Development Installation

```bash
# Clone the repository
git clone https://github.com/dianbrown/QuantumQueue.git
cd QuantumQueue

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## ✨ Features

### CPU Scheduling Algorithms
- **First Come First Served (FCFS)** - Basic FIFO scheduling
- **FCFS with Priority** - Priority-based FCFS
- **Shortest Job First (SJF)** - Non-preemptive shortest job first
- **SJF with Priority** - Priority-based SJF
- **Shortest Remaining Time (SRT)** - Preemptive SJF
- **Round Robin (RR)** - Time-quantum based scheduling
- **Round Robin with Priority** - Priority-based Round Robin

### Page Replacement Algorithms
- **First In First Out (FIFO)** - Basic queue-based replacement
- **Least Recently Used (LRU)** - Recency-based replacement
- **Optimal** - Theoretical best performance
- **Second Chance** - Enhanced FIFO with reference bit
- **Clock** - Circular queue variant

### Interactive Features
- 🎨 **28 Beautiful Themes** (Dracula, Nord, Tokyo Night, and more)
- 📊 **Visual Gantt Charts** for CPU scheduling
- 🎯 **Step-by-step Tutorials** for every algorithm
- 🔄 **Random Test Case Generation**
- 📝 **Editable Process/Frame Tables**
- 📈 **Real-time Performance Metrics**
- 🎭 **Drag-and-Drop Interface** for page replacement
- 💾 **Persistent Settings** across sessions

## 📸 Screenshots

*Coming soon*

## 🚀 Usage

### CPU Scheduling Practice
1. **Select an algorithm** from the dropdown
2. **Add processes** manually or use "Random Processes"
3. **Edit** arrival times, burst times, and priorities
4. **Click "Simulate"** to see the Gantt chart
5. **Review** waiting times, turnaround times, and metrics

### Page Replacement Practice
1. **Select an algorithm** from the dropdown
2. **Set the number of frames**
3. **Enter page sequence** or use "Random Sequence"
4. **Click "Run Algorithm"** to visualize
5. **Review** page faults, hits, and hit ratio

### Tutorials
1. **Click the Help icon** in the sidebar
2. **Select CPU or PRA** category
3. **Choose an algorithm** to learn
4. **Follow step-by-step examples** with interactive visualizations

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
