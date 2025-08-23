"""Scheduling result data model."""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ProcessMetrics:
    """Metrics for a single process."""
    start: Optional[int] = None
    end: Optional[int] = None
    waiting: int = 0
    turnaround: int = 0


@dataclass
class SchedulingResult:
    """Result of a scheduling algorithm execution.
    
    Attributes:
        timeline: List representing the timeline, where each index is a time unit
                 and the value is the process ID running at that time
        process_metrics: Dictionary mapping process IDs to their metrics
        algorithm_name: Name of the scheduling algorithm used
    """
    timeline: List[Optional[str]]
    process_metrics: Dict[str, ProcessMetrics]
    algorithm_name: str = ""
    
    def get_average_waiting_time(self) -> float:
        """Calculate average waiting time across all processes."""
        if not self.process_metrics:
            return 0.0
        total_waiting = sum(metrics.waiting for metrics in self.process_metrics.values())
        return total_waiting / len(self.process_metrics)
    
    def get_average_turnaround_time(self) -> float:
        """Calculate average turnaround time across all processes."""
        if not self.process_metrics:
            return 0.0
        total_turnaround = sum(metrics.turnaround for metrics in self.process_metrics.values())
        return total_turnaround / len(self.process_metrics)
