# CPU Scheduling Practice Application

A comprehensive Qt-based application for practicing various CPU scheduling algorithms.

## Project Structure

```
CPU_SchedulingPython/
├── main_new.py              # Main entry point
├── main.py                  # Legacy main file (can be removed)
├── requirements.txt         # Python dependencies
├── models/                  # Data models
│   ├── __init__.py
│   ├── process.py          # Process data class
│   └── scheduling_result.py # Result data class
├── algorithms/              # Scheduling algorithms
│   ├── __init__.py
│   ├── base_scheduler.py   # Abstract base class
│   ├── fcfs.py            # First Come First Served
│   ├── fcfs_priority.py   # FCFS with Priority
│   ├── round_robin.py     # Round Robin (template)
│   ├── sjf.py            # Shortest Job First (template)
│   └── srt.py            # Shortest Remaining Time (template)
├── ui/                     # User interface components
│   ├── __init__.py
│   └── main_window.py     # Main application window
└── utils/                  # Utility functions
    ├── __init__.py
    └── process_generator.py # Random process generator
```

## Features

### Current Implementation
- ✅ **FCFS (First Come First Served)**: Non-preemptive scheduling
- ✅ **FCFS with Priority**: Preemptive priority scheduling
- ✅ **Smart Process Generation**: Eliminates some random gaps for better visualization
- ✅ **Interactive Timeline**: Click and double-click to fill cells
- ✅ **Solution Checking**: Compare your input with the correct solution
- ✅ **Metrics Display**: Waiting time, turnaround time, averages

### Future Algorithms to implement
- 🔲 **Round Robin (RR)**: Time quantum-based scheduling
- 🔲 **Round Robin with Priority (RRP)**: Priority + time quantum
- 🔲 **Shortest Job First (SJF)**: Non-preemptive shortest job
- 🔲 **SJF with Priority (SJFP)**: Priority + shortest job
- 🔲 **Shortest Remaining Time (SRT)**: Preemptive shortest remaining time

## Usage

### Running the Application
```bash
python main_new.py
```

### Adding New Algorithms
1. Create a new file in `algorithms/` directory
2. Inherit from `BaseScheduler`
3. Implement the `schedule()` method
4. Add to the schedulers dictionary in `main_window.py`

### Example Algorithm Implementation
```python
from .base_scheduler import BaseScheduler
from models.process import Process
from models.scheduling_result import SchedulingResult

class MyScheduler(BaseScheduler):
    @property
    def name(self) -> str:
        return "My Algorithm"
    
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        # Implement your algorithm logic here
        timeline = [None] * 32
        metrics = self._calculate_metrics(processes, timeline, start_times, end_times)
        return SchedulingResult(timeline, metrics, self.name)
```

## Architecture Benefits

### Separation of Concerns
- **Models**: Pure data classes with no business logic
- **Algorithms**: Independent scheduling implementations
- **UI**: Clean interface separate from algorithm logic
- **Utils**: Reusable utility functions

### Extensibility
- Easy to add new scheduling algorithms
- Algorithms are self-contained and testable
- Common functionality shared through base class
- UI automatically supports new algorithms

## Key Classes

### Process
Represents a single process with:
- `id`: Process identifier (A, B, C, etc.)
- `priority`: Priority level
- `arrival`: Arrival time
- `burst`: CPU burst time required

### SchedulingResult
Contains the results of algorithm execution:
- `timeline`: List of process IDs at each time unit
- `process_metrics`: Waiting/turnaround times per process
- `algorithm_name`: Name of the algorithm used

### BaseScheduler
Abstract base class providing:
- Common interface for all algorithms
- Shared metric calculation utilities
- Template for algorithm implementation
