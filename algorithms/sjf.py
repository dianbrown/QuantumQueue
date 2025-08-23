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
        
        Args:
            processes: List of processes to schedule
            
        Returns:
            SchedulingResult containing timeline and metrics
        """
        if not processes:
            return SchedulingResult([], {}, self.name)
        
        # TODO: Implement SJF algorithm
        # This is a placeholder for future implementation
        timeline = [None] * 32
        metrics = {}
        
        return SchedulingResult(timeline, metrics, self.name)
