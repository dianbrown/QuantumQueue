"""Shortest Job First (SJF) scheduling algorithm."""

from typing import List, Optional
from .base_scheduler import BaseScheduler
from models.process import Process
from models.scheduling_result import SchedulingResult


class SJFScheduler(BaseScheduler):
    """Shortest Job First scheduling algorithm."""
    
    @property
    def name(self) -> str:
        return "SJF"
    
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        """Execute SJF scheduling algorithm.
        
        Algorithm:
        1. Always select the process with the shortest burst time from ready processes
        2. Process runs to completion (non-preemptive)
        3. When multiple processes have same burst time, use arrival time as tie-breaker
        
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
            remaining_processes.append(Process(p.id, p.priority, p.arrival, p.burst))
        
        # Sort by arrival time for easy processing
        remaining_processes.sort(key=lambda p: (p.arrival, p.id))
        
        ready_queue = []
        current_time = 1
        start_times = {}
        end_times = {}
        
        while current_time <= 32:
            # Add newly arrived processes to ready queue
            while remaining_processes and remaining_processes[0].arrival <= current_time:
                new_process = remaining_processes.pop(0)
                ready_queue.append(new_process)
            
            # Select process with shortest burst time from ready queue
            if ready_queue:
                # Sort by burst time (shortest first), then by arrival time for tie-breaking
                ready_queue.sort(key=lambda p: (p.burst, p.arrival, p.id))
                current_process = ready_queue.pop(0)
                
                # Record start time
                start_times[current_process.id] = current_time
                
                # Execute process to completion
                while current_process.burst > 0 and current_time <= 32:
                    # Place process in timeline
                    timeline_index = current_time - 1
                    if timeline_index < len(timeline):
                        timeline[timeline_index] = current_process.id
                    
                    # Consume time
                    current_process.burst -= 1
                    current_time += 1
                
                # Record end time
                end_times[current_process.id] = current_time
            else:
                # No processes ready, advance time
                current_time += 1
            
            # Break if no more work to do
            if not remaining_processes and not ready_queue:
                break
        
        # Calculate metrics using original burst times
        processes_for_metrics = []
        for p in processes:
            processes_for_metrics.append(Process(p.id, p.priority, p.arrival, original_bursts[p.id]))
        
        process_metrics = self._calculate_metrics(processes_for_metrics, timeline, start_times, end_times)
        
        return SchedulingResult(timeline, process_metrics, self.name)
