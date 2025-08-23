"""Shortest Remaining Time (SRT) scheduling algorithm."""

from typing import List, Optional
from .base_scheduler import BaseScheduler
from models.process import Process
from models.scheduling_result import SchedulingResult


class SRTScheduler(BaseScheduler):
    """Shortest Remaining Time scheduling algorithm."""
    
    @property
    def name(self) -> str:
        return "SRT"
    
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        """Execute SRT scheduling algorithm.
        
        Args:
            processes: List of processes to schedule
            
        Returns:
            SchedulingResult containing timeline and metrics
        """
        if not processes:
            return SchedulingResult([], {}, self.name)
        
        # TODO: Implement SRT algorithm
        # This is a placeholder for future implementation
        timeline = [None] * 32
        metrics = {}
        
        return SchedulingResult(timeline, metrics, self.name)
