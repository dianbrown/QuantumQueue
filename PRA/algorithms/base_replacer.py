"""Base class for Page Replacement Algorithms."""

from abc import ABC, abstractmethod
from typing import List, Tuple
from .models.page_result import PageResult


class BasePageReplacer(ABC):
    """Abstract base class for all page replacement algorithms."""
    
    @abstractmethod
    def replace_pages(self, page_references: List[int], frame_count: int) -> PageResult:
        """Execute the page replacement algorithm.
        
        Args:
            page_references: List of page references
            frame_count: Number of available frames
            
        Returns:
            PageResult containing algorithm results
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the algorithm name."""
        pass
