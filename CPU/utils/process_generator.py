"""Process generator utility for creating randomized processes."""

import random
from typing import List
from ..models.process import Process


class ProcessGenerator:
    """Utility class for generating randomized processes."""
    
    @staticmethod
    def generate_processes(num_processes: int = None, unique_arrivals: bool = False) -> List[Process]:
        """Generate a list of randomized processes with intelligent arrival times.
        
        Args:
            num_processes: Number of processes to generate. If None, generates 3-7 processes.
            unique_arrivals: If True, ensures all processes have unique arrival times.
            
        Returns:
            List of Process objects with optimized arrival times and burst times that fit in timeline.
        """
        if num_processes is None:
            num_processes = random.randint(3, 7)
        
        # Maximum timeline length (32 columns)
        MAX_TIMELINE = 32
        
        # Reserve some space for gaps and arrival times (use 80% of timeline for burst times)
        max_total_burst = int(MAX_TIMELINE * 0.8)
        
        processes = []
        total_burst_so_far = 0
        
        # Create processes A, B, C, D, E, F, G in order (top to bottom)
        for i in range(num_processes):
            process_id = chr(ord('A') + i)
            priority = random.randint(1, 5)
            
            # Calculate remaining burst time budget
            remaining_processes = num_processes - i
            remaining_burst_budget = max_total_burst - total_burst_so_far
            
            # Ensure minimum burst time of 1 for remaining processes
            min_burst_needed_for_others = remaining_processes - 1
            available_for_this_process = remaining_burst_budget - min_burst_needed_for_others
            
            # Set burst time constraints
            min_burst = 1
            max_burst = max(min_burst, min(5, available_for_this_process))
            
            # For the last process, use exactly what's left (if reasonable)
            if i == num_processes - 1:
                burst = max(1, min(remaining_burst_budget, 5))
            else:
                burst = random.randint(min_burst, max_burst)
            
            total_burst_so_far += burst
            processes.append(Process(process_id, priority, 0, burst))  # Temporary arrival time
        
        # Generate arrival times (unique if requested)
        if unique_arrivals:
            # Generate unique arrival times
            used_arrivals = set()
            max_arrival = min(8, MAX_TIMELINE - total_burst_so_far)
            
            for i, process in enumerate(processes):
                if i == num_processes - 1:
                    # Last process gets arrival time 1
                    arrival = 1
                else:
                    # Find an unused arrival time
                    attempts = 0
                    while attempts < 50:  # Prevent infinite loop
                        arrival = random.randint(2, max(2, max_arrival))
                        if arrival not in used_arrivals and arrival != 1:  # Don't use 1 (reserved for last)
                            break
                        attempts += 1
                    else:
                        # If we can't find unique time, use sequential assignment
                        arrival = 2 + i
                
                used_arrivals.add(arrival)
                process.arrival = arrival
        else:
            # Original logic - allow duplicate arrival times
            for i, process in enumerate(processes):
                if i == num_processes - 1:
                    arrival = 1
                else:
                    max_arrival = min(8, MAX_TIMELINE - total_burst_so_far)
                    arrival = random.randint(2, max(2, max_arrival))
                process.arrival = arrival
        
        # Apply intelligent gap elimination
        return ProcessGenerator._eliminate_gaps(processes)
    
    @staticmethod
    def _eliminate_gaps(processes: List[Process]) -> List[Process]:
        """Intelligently adjust arrival times to eliminate gaps in scheduling.
        
        Args:
            processes: List of processes to optimize
            
        Returns:
            List of processes with optimized arrival times that fit in timeline
        """
        MAX_TIMELINE = 32
        
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
            # But ensure we don't exceed timeline limits
            if current_time >= MAX_TIMELINE - 2:  # Leave some buffer
                # If we're near the timeline limit, make remaining processes arrive earlier
                optimal_arrival = min(process.arrival, current_time - 1)
            else:
                optimal_arrival = min(process.arrival, current_time)
            
            # Ensure arrival time is reasonable
            new_arrival = max(1, min(optimal_arrival, MAX_TIMELINE - process.burst - 1))
            
            new_processes.append(Process(process.id, process.priority, new_arrival, process.burst))
            
            # Update current_time based on when this process would finish
            process_start = max(new_arrival, current_time)
            current_time = min(process_start + process.burst, MAX_TIMELINE)
        
        # Sort back to A, B, C, D order for display (not by arrival time)
        return sorted(new_processes, key=lambda p: p.id)
    
    @staticmethod
    def _validate_timeline_fit(processes: List[Process]) -> bool:
        """Validate that processes can fit within the 32-column timeline.
        
        Args:
            processes: List of processes to validate
            
        Returns:
            True if processes fit within timeline, False otherwise
        """
        MAX_TIMELINE = 32
        
        # Check total burst time
        total_burst = sum(p.burst for p in processes)
        if total_burst > MAX_TIMELINE:
            return False
        
        # Check that no process arrives too late
        max_arrival = max(p.arrival for p in processes)
        min_burst_after_max_arrival = min(p.burst for p in processes if p.arrival == max_arrival)
        
        if max_arrival + min_burst_after_max_arrival > MAX_TIMELINE:
            return False
        
        return True
    
    @staticmethod
    def generate_quantum() -> int:
        """Generate a random time quantum for Round Robin algorithms.
        
        Returns:
            Random quantum value between 1 and 5
        """
        return random.randint(1, 5)
