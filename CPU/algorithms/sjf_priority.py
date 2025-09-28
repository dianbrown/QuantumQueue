"""SJF with Priority scheduling algorithm."""

from typing import List, Optional
from .base_scheduler import BaseScheduler
from ..models.process import Process
from ..models.scheduling_result import SchedulingResult


class SJFPriorityScheduler(BaseScheduler):
    """SJF with Priority scheduling algorithm."""
    
    @property
    def name(self) -> str:
        return "SJF Priority"
    
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        """Execute SJF with Priority scheduling algorithm.
        
        Algorithm:
        1. Higher priority numbers can interrupt lower priority numbers (preemptive)
        2. Same priority numbers use SJF logic (shortest burst time wins)
        3. Process selection: Priority first, then shortest burst time
        
        Args:
            processes: List of processes to schedule
            
        Returns:
            SchedulingResult containing timeline and metrics
        """
        if not processes:
            return SchedulingResult([], {}, self.name)
        
        # Create timeline - index i represents time i+1 in the grid
        timeline = [None] * 32
        
        # Store original burst times for metrics calculation
        original_bursts = {}
        for p in processes:
            original_bursts[p.id] = p.burst
        
        # Create working copies to avoid modifying originals
        remaining_processes = []
        for p in processes:
            proc = Process(p.id, p.priority, p.arrival, p.burst)
            proc.original_burst = p.burst  # Store original burst time for comparison
            remaining_processes.append(proc)
        
        # Sort by arrival time for easy processing
        remaining_processes.sort(key=lambda p: (p.arrival, p.id))
        
        ready_queue = []
        current_time = 1
        start_times = {}
        end_times = {}
        current_process = None
        
        while current_time <= 32:
            # Add newly arrived processes to ready queue and check for preemption
            while remaining_processes and remaining_processes[0].arrival <= current_time:
                new_process = remaining_processes.pop(0)
                ready_queue.append(new_process)
                
                # Check if this new process can preempt current process
                if current_process:
                    if (new_process.priority > current_process.priority or 
                        (new_process.priority == current_process.priority and 
                         new_process.original_burst < current_process.original_burst)):
                        # Higher priority or same priority with shorter original burst - preempt immediately
                        ready_queue.append(current_process)
                        current_process = None
                        break  # Break to handle preemption immediately
            
            # If no current process, select one from ready queue
            if current_process is None and ready_queue:
                # Sort by priority (descending), then by original burst time (ascending), then by arrival
                ready_queue.sort(key=lambda p: (-p.priority, p.original_burst, p.arrival, p.id))
                current_process = ready_queue.pop(0)
                
                # Record start time only for the first time this process runs
                if current_process.id not in start_times:
                    start_times[current_process.id] = current_time
            
            # Execute current process if available
            if current_process:
                # Place process in timeline
                timeline_index = current_time - 1
                if timeline_index < len(timeline):
                    timeline[timeline_index] = current_process.id
                
                # Consume time
                current_process.burst -= 1
                current_time += 1
                
                # Check if process finished
                if current_process.burst == 0:
                    end_times[current_process.id] = current_time
                    current_process = None
            else:
                # No processes ready, advance time
                current_time += 1
            
            # Break if no more work to do
            if not remaining_processes and not ready_queue and current_process is None:
                break
        
        # Calculate metrics using original burst times
        processes_for_metrics = []
        for p in processes:
            processes_for_metrics.append(Process(p.id, p.priority, p.arrival, original_bursts[p.id]))
        
        process_metrics = self._calculate_metrics(processes_for_metrics, timeline, start_times, end_times)
        
        return SchedulingResult(timeline, process_metrics, self.name)
