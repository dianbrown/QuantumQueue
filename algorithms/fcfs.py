"""First Come First Served (FCFS) scheduling algorithm."""

from typing import List, Optional
from .base_scheduler import BaseScheduler
from models.process import Process
from models.scheduling_result import SchedulingResult


class FCFSScheduler(BaseScheduler):
    """First Come First Served scheduling algorithm."""
    
    @property
    def name(self) -> str:
        return "FCFS"
    
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        """Execute FCFS scheduling algorithm.
        
        Args:
            processes: List of processes to schedule
            
        Returns:
            SchedulingResult containing timeline and metrics
        """
        if not processes:
            return SchedulingResult([], {}, self.name)
        
        # Sort by arrival time, then by process ID for tie-breaking
        sorted_processes = sorted(processes, key=lambda p: (p.arrival, p.id))
        
        # Create timeline - index i represents time i+1 in the grid
        timeline = [None] * 32
        
        current_time = 1  # Start from time 1 to match grid headers
        start_times = {}
        end_times = {}
        
        # Process each process in FCFS order
        for process in sorted_processes:
            # If current time is before process arrival, advance to arrival time
            if current_time < process.arrival:
                current_time = process.arrival
            
            # Record start time
            start_times[process.id] = current_time
            
            # Execute the process for its burst time
            for i in range(process.burst):
                timeline_index = current_time - 1  # Convert to 0-based index
                if timeline_index < len(timeline):
                    timeline[timeline_index] = process.id
                current_time += 1
            
            # Record end time
            end_times[process.id] = current_time
        
        # Calculate metrics
        metrics = self._calculate_metrics(processes, timeline, start_times, end_times)
        
        return SchedulingResult(timeline, metrics, self.name)
