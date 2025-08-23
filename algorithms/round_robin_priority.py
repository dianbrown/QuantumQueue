"""Round Robin with Priority scheduling algorithm."""

from typing import List, Optional
from .base_scheduler import BaseScheduler
from models.process import Process
from models.scheduling_result import SchedulingResult


class RoundRobinPriorityScheduler(BaseScheduler):
    """Round Robin with Priority scheduling algorithm."""
    
    def __init__(self, time_quantum: int = 2):
        """Initialize the scheduler.
        
        Args:
            time_quantum: Time slice for each process
        """
        self.time_quantum = time_quantum
    
    @property
    def name(self) -> str:
        return f"Round Robin Priority (Q={self.time_quantum})"
    
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        """Execute Round Robin with Priority scheduling algorithm.
        
        Algorithm:
        1. Higher priority numbers can interrupt lower priority numbers (even mid-quantum)
        2. Same priority numbers follow regular Round Robin rules:
           - Use Ready State (RS) times
           - Complete full quantum cycles
           - No interruption between same priority processes
        3. Initially RS = arrival time
        4. After quantum, new RS = current time when quantum ends
        
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
        current_process = None
        quantum_used = 0
        
        while current_time <= 32:
            # Add newly arrived processes to ready queue
            while remaining_processes and remaining_processes[0].arrival <= current_time:
                new_process = remaining_processes.pop(0)
                ready_queue.append(new_process)
                
                # Check if this new process can preempt current process
                if current_process and new_process.priority > current_process.priority:
                    # Higher priority process arrived - preempt current process
                    current_process.ready_state = current_time
                    ready_queue.append(current_process)
                    current_process = None
                    quantum_used = 0
            
            # If no current process, select one from ready queue
            if current_process is None and ready_queue:
                # First, get highest priority processes
                max_priority = max(p.priority for p in ready_queue)
                highest_priority_processes = [p for p in ready_queue if p.priority == max_priority]
                
                # Among highest priority, use Ready State rules
                highest_priority_processes.sort(key=lambda p: (p.ready_state, -p.arrival))
                current_process = highest_priority_processes[0]
                ready_queue.remove(current_process)
                
                # Record start time only for the first time this process runs
                if current_process.id not in start_times:
                    start_times[current_process.id] = current_time
                
                quantum_used = 0
            
            # Execute current process if available
            if current_process:
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
                    current_process = None
                    quantum_used = 0
                # Check if quantum expired
                elif quantum_used >= self.time_quantum:
                    # Quantum expired - move to ready queue with new Ready State
                    current_process.ready_state = current_time
                    ready_queue.append(current_process)
                    current_process = None
                    quantum_used = 0
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
