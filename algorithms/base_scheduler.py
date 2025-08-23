"""Base scheduler class for all CPU scheduling algorithms."""

from abc import ABC, abstractmethod
from typing import List
from models.process import Process
from models.scheduling_result import SchedulingResult


class BaseScheduler(ABC):
    """Abstract base class for all CPU scheduling algorithms."""
    
    @abstractmethod
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        """Execute the scheduling algorithm.
        
        Args:
            processes: List of processes to schedule
            
        Returns:
            SchedulingResult containing timeline and metrics
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the scheduling algorithm."""
        pass
    
    def _calculate_metrics(self, processes: List[Process], timeline: List[str], 
                          start_times: dict, end_times: dict) -> dict:
        """Helper method to calculate waiting and turnaround times.
        
        Args:
            processes: Original list of processes
            timeline: Execution timeline
            start_times: Dictionary of process start times
            end_times: Dictionary of process end times
            
        Returns:
            Dictionary of process metrics
        """
        from models.scheduling_result import ProcessMetrics
        
        metrics = {}
        original_bursts = {p.id: p.burst for p in processes}
        
        for process in processes:
            pid = process.id
            if pid in start_times and pid in end_times:
                turnaround = end_times[pid] - process.arrival
                waiting = turnaround - original_bursts[pid]
                
                metrics[pid] = ProcessMetrics(
                    start=start_times[pid],
                    end=end_times[pid],
                    waiting=max(0, waiting),  # Ensure non-negative
                    turnaround=turnaround
                )
            else:
                # Process didn't execute
                metrics[pid] = ProcessMetrics()
        
        return metrics
