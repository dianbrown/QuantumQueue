"""FIFO (First In, First Out) page replacement algorithm."""

from typing import List, Optional, Deque
from collections import deque
from .base_replacer import BaseReplacer, PageReplacementResult


class FIFOReplacer(BaseReplacer):
    """FIFO page replacement algorithm implementation."""
    
    def get_algorithm_name(self) -> str:
        """Get the name of the algorithm."""
        return "FIFO"
        
    def replace_pages_with_frames(self, page_sequence: List[str], frames_data: List) -> PageReplacementResult:
        """
        Execute FIFO page replacement algorithm with initial frame data.
        
        Args:
            page_sequence: List of page IDs to access
            frames_data: List of Frame objects with initial state
            
        Returns:
            PageReplacementResult with complete execution details
        """
        num_frames = len(frames_data)
        result = PageReplacementResult(page_sequence, num_frames)
        
        # Sort frames by load time to establish FIFO queue order
        sorted_frames = sorted(frames_data, key=lambda f: f.load_time)
        
        # Initialize frame states with their initial pages
        frame_pages = {}  # frame_id -> current_page
        frame_queue = deque()  # Queue of frame_ids in FIFO order
        
        for frame in sorted_frames:
            frame_pages[frame.frame_id] = frame.pages_in_memory if frame.pages_in_memory else None
            frame_queue.append(frame.frame_id)
        
        # Process each page request
        for time, page_id in enumerate(page_sequence):
            # Check if page is already in memory (page hit)
            current_pages = [frame_pages[frame.frame_id] for frame in frames_data]
            is_hit = page_id in current_pages
            
            if is_hit:
                # Page hit - no replacement needed, queue order stays the same
                pass
            else:
                # Page fault - replace page in oldest frame (front of queue)
                oldest_frame_id = frame_queue.popleft()  # Remove from front
                frame_pages[oldest_frame_id] = page_id   # Replace page
                frame_queue.append(oldest_frame_id)      # Move to back of queue
            
            # Record the access result with current frame state (in original order)
            current_state = [frame_pages[frame.frame_id] for frame in frames_data]
            result.add_access(page_id, time, is_hit, current_state)
            
        return result
        
    def replace_pages(self, page_sequence: List[str], num_frames: int) -> PageReplacementResult:
        """
        Legacy method for backward compatibility.
        """
        # Create dummy frames for compatibility
        from ..models.frame import Frame
        frames_data = [Frame(str(i), i, "") for i in range(num_frames)]
        return self.replace_pages_with_frames(page_sequence, frames_data)
