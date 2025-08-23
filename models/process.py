"""Process data model for CPU Scheduling."""

from dataclasses import dataclass


@dataclass
class Process:
    """Represents a process in CPU scheduling.
    
    Attributes:
        id: Unique identifier for the process (e.g., 'A', 'B', 'C')
        priority: Priority level (higher number = higher priority)
        arrival: Arrival time when process enters the system
        burst: CPU burst time required by the process
    """
    id: str
    priority: int
    arrival: int
    burst: int
    
    def __str__(self):
        return f"Process {self.id}: Priority={self.priority}, Arrival={self.arrival}, Burst={self.burst}"
    
    def __repr__(self):
        return f"Process(id='{self.id}', priority={self.priority}, arrival={self.arrival}, burst={self.burst})"
