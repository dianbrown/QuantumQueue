"""First Come First Served with Priority scheduling algorithm."""

from typing import List, Optional
from .base_scheduler import BaseScheduler
from ..models.process import Process
from ..models.scheduling_result import SchedulingResult


class FCFSPriorityScheduler(BaseScheduler):
    """First Come First Served with Priority (Preemptive) scheduling algorithm."""
    
    def __init__(self, higher_is_better: bool = True):
        """Initialize the scheduler.
        
        Args:
            higher_is_better: If True, higher priority numbers are better.
                            If False, lower priority numbers are better.
        """
        self.higher_is_better = higher_is_better
    
    @property
    def name(self) -> str:
        return "FCFS with Priority"
    
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        """Execute FCFS with Priority scheduling algorithm.
        
        Args:
            processes: List of processes to schedule
            
        Returns:
            SchedulingResult containing timeline and metrics
        """
        if not processes:
            return SchedulingResult([], {}, self.name)
        
        # Create timeline - index i represents time i+1 in the grid
        timeline = [None] * 32
        
        # Create a copy of processes to avoid modifying originals
        process_copies = []
        for p in processes:
            process_copies.append(Process(p.id, p.priority, p.arrival, p.burst))
        
        remaining_processes = sorted(process_copies, key=lambda p: (p.arrival, p.id))
        ready_queue = []
        current_time = 1  # Start from time 1 to match grid headers
        start_times = {}
        end_times = {}
        
        current_process = None
        current_burst_left = 0
        
        while current_time <= 32 and (remaining_processes or current_process or ready_queue):
            # Add newly arrived processes to ready queue
            while remaining_processes and remaining_processes[0].arrival <= current_time:
                new_process = remaining_processes.pop(0)
                ready_queue.append(new_process)
                
                # Preemption check: if new process has higher priority than current
                if (current_process and 
                    ((self.higher_is_better and new_process.priority > current_process.priority) or
                     (not self.higher_is_better and new_process.priority < current_process.priority))):
                    # Preempt current process - save remaining burst time
                    current_process.burst = current_burst_left
                    ready_queue.append(current_process)
                    current_process = None
            
            # Sort ready queue by priority, then by arrival time (FCFS for same priority)
            if self.higher_is_better:
                ready_queue.sort(key=lambda p: (-p.priority, p.arrival, p.id))
            else:
                ready_queue.sort(key=lambda p: (p.priority, p.arrival, p.id))
            
            # If no current process and ready queue has processes
            if not current_process and ready_queue:
                current_process = ready_queue.pop(0)
                current_burst_left = current_process.burst
                if current_process.id not in start_times:
                    start_times[current_process.id] = current_time
            
            # Execute current process
            if current_process:
                timeline_index = current_time - 1  # Convert to 0-based index
                if timeline_index < len(timeline):
                    timeline[timeline_index] = current_process.id
                current_burst_left -= 1
                
                if current_burst_left == 0:
                    end_times[current_process.id] = current_time + 1
                    current_process = None
            
            current_time += 1
        
        # Calculate metrics using original burst times
        metrics = self._calculate_metrics(processes, timeline, start_times, end_times)
        
        return SchedulingResult(timeline, metrics, self.name)
