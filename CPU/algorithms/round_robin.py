"""Round Robin (RR) scheduling algorithm."""

from typing import List, Optional
from .base_scheduler import BaseScheduler
from ..models.process import Process
from ..models.scheduling_result import SchedulingResult


class RoundRobinScheduler(BaseScheduler):
    """Round Robin scheduling algorithm."""
    
    def __init__(self, time_quantum: int = 2):
        """Initialize the scheduler.
        
        Args:
            time_quantum: Time slice for each process
        """
        self.time_quantum = time_quantum
    
    @property
    def name(self) -> str:
        return f"Round Robin (Q={self.time_quantum})"
    
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        """Execute Round Robin scheduling algorithm with Ready State priority.
        
        Algorithm:
        1. Each process has a Ready State (RS) time when it becomes ready
        2. Initially RS = arrival time  
        3. After using quantum, new RS = current time when quantum ends
        4. Always pick process with earliest RS time
        5. If tie in RS time, pick newest arrival (most recently arrived)
        
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
        
        # Create working copies with Ready State tracking
        remaining_processes = []
        for p in processes:
            proc = Process(p.id, p.priority, p.arrival, p.burst)
            proc.ready_state = p.arrival  # Add ready state tracking
            remaining_processes.append(proc)
        
        # Sort by arrival time
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
            
            # Pick process with earliest Ready State time
            # If tie, pick the newest arrival (most recently arrived)
            if ready_queue:
                # Sort by Ready State time, then by arrival time (descending for newest first)
                ready_queue.sort(key=lambda p: (p.ready_state, -p.arrival))
                current_process = ready_queue.pop(0)
                
                # Record start time only for the first time this process runs
                if current_process.id not in start_times:
                    start_times[current_process.id] = current_time
                
                # Execute for quantum (or until process finishes)
                quantum_used = 0
                start_time = current_time
                
                while quantum_used < self.time_quantum and current_process.burst > 0 and current_time <= 32:
                    # Place process in timeline
                    timeline_index = current_time - 1
                    if timeline_index < len(timeline):
                        timeline[timeline_index] = current_process.id
                    
                    # Consume time
                    current_process.burst -= 1
                    quantum_used += 1
                    current_time += 1
                
                # Check if process finished
                if current_process.burst == 0:
                    end_times[current_process.id] = current_time
                else:
                    # Process still has work, update its Ready State to current time
                    current_process.ready_state = current_time
                    ready_queue.append(current_process)
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
