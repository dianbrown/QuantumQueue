"""Process generator utility for creating randomized processes."""

import random
from typing import List
from models.process import Process


class ProcessGenerator:
    """Utility class for generating randomized processes."""
    
    @staticmethod
    def generate_processes(num_processes: int = None) -> List[Process]:
        """Generate a list of randomized processes with intelligent arrival times.
        
        Args:
            num_processes: Number of processes to generate. If None, generates 3-7 processes.
            
        Returns:
            List of Process objects with optimized arrival times for continuous scheduling.
        """
        if num_processes is None:
            num_processes = random.randint(3, 7)
        
        processes = []
        
        # Create processes A, B, C, D, E, F, G in order (top to bottom)
        for i in range(num_processes):
            process_id = chr(ord('A') + i)
            priority = random.randint(1, 5)
            burst = random.randint(2, 5)  # Smaller burst times for better continuity
            
            # The LAST process (bottom one) gets arrival time 1
            if i == num_processes - 1:
                arrival = 1
            else:
                # Other processes get strategic arrival times
                arrival = random.randint(2, 8)
            
            processes.append(Process(process_id, priority, arrival, burst))
        
        # Apply intelligent gap elimination
        return ProcessGenerator._eliminate_gaps(processes)
    
    @staticmethod
    def _eliminate_gaps(processes: List[Process]) -> List[Process]:
        """Intelligently adjust arrival times to eliminate gaps in scheduling.
        
        Args:
            processes: List of processes to optimize
            
        Returns:
            List of processes with optimized arrival times
        """
        # Sort by current arrival times to see the timeline
        sorted_by_arrival = sorted(processes, key=lambda p: p.arrival)
        
        # Find the process with arrival time 1 (our anchor)
        anchor_process = next(p for p in sorted_by_arrival if p.arrival == 1)
        current_time = 1
        
        # Create a new timeline starting from time 1
        new_processes = []
        processed_ids = set()
        
        # Start with the anchor process
        new_processes.append(Process(anchor_process.id, anchor_process.priority, 1, anchor_process.burst))
        processed_ids.add(anchor_process.id)
        current_time += anchor_process.burst
        
        # Sort remaining processes by their original arrival times
        remaining = [p for p in sorted_by_arrival if p.id not in processed_ids]
        
        for process in remaining:
            # Calculate when this process should arrive to minimize gaps
            # It should arrive no later than current_time to avoid gaps
            optimal_arrival = min(process.arrival, current_time)
            
            # But ensure it doesn't arrive before its original time if that would make sense
            if process.arrival <= current_time + 1:  # Allow small gaps (1 unit max)
                new_arrival = process.arrival
            else:
                # Bring it closer to eliminate larger gaps
                new_arrival = current_time + random.randint(0, 1)
            
            new_processes.append(Process(process.id, process.priority, new_arrival, process.burst))
            # Update current_time based on when this process would finish
            process_start = max(new_arrival, current_time)
            current_time = process_start + process.burst
        
        # Sort back to A, B, C, D order for display (not by arrival time)
        return sorted(new_processes, key=lambda p: p.id)
    
    @staticmethod
    def generate_quantum() -> int:
        """Generate a random time quantum for Round Robin algorithms.
        
        Returns:
            Random quantum value between 1 and 5
        """
        return random.randint(1, 5)
