"""Page replacement result model."""

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class PageResult:
    """Result of a page replacement algorithm execution."""
    
    frames_timeline: List[List[int]]  # Frame states at each step
    page_references: List[int]        # Original page references
    page_faults: List[bool]          # Whether each reference caused a fault
    algorithm_name: str              # Name of the algorithm used
    
    @property
    def total_page_faults(self) -> int:
        """Get total number of page faults."""
        return sum(self.page_faults)
    
    @property
    def page_fault_rate(self) -> float:
        """Get page fault rate as percentage."""
        if not self.page_references:
            return 0.0
        return (self.total_page_faults / len(self.page_references)) * 100
