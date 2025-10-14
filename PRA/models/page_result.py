"""Page replacement result model."""

from typing import List, Dict, Optional
from dataclasses import dataclass


class PageAccessResult:
    """Represents the result of a single page access."""
    
    def __init__(self, page_id: str, time: int, is_hit: bool, frames_state: List[Optional[str]]):
        self.page_id = page_id
        self.time = time
        self.is_hit = is_hit
        self.frames_state = frames_state.copy()  # State of all frames after this access


class PageReplacementResult:
    """Complete result of page replacement algorithm execution."""
    
    def __init__(self, page_sequence: List[str], num_frames: int):
        self.page_sequence = page_sequence
        self.num_frames = num_frames
        self.accesses: List[PageAccessResult] = []
        self.page_faults = 0
        self.page_hits = 0
        
    def add_access(self, page_id: str, time: int, is_hit: bool, frames_state: List[Optional[str]]):
        """Add a page access result."""
        access = PageAccessResult(page_id, time, is_hit, frames_state)
        self.accesses.append(access)
        
        if is_hit:
            self.page_hits += 1
        else:
            self.page_faults += 1
            
    def get_hit_ratio(self) -> float:
        """Calculate the page hit ratio."""
        total_accesses = len(self.accesses)
        return (self.page_hits / total_accesses) if total_accesses > 0 else 0.0
        
    def get_fault_ratio(self) -> float:
        """Calculate the page fault ratio."""
        total_accesses = len(self.accesses)
        return (self.page_faults / total_accesses) if total_accesses > 0 else 0.0
