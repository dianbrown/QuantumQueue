"""Frame model for Page Replacement Algorithms."""

from typing import Optional


class Frame:
    """Represents a memory frame in page replacement."""
    
    def __init__(self, frame_id: str, load_time: int = 0, pages_in_memory: str = ""):
        self.frame_id = frame_id
        self.load_time = load_time
        self.pages_in_memory = pages_in_memory
        
    def __str__(self):
        return f"Frame {self.frame_id}: Load={self.load_time}, Pages={self.pages_in_memory}"
