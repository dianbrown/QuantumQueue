"""LRU (Least Recently Used) page replacement algorithm."""

from typing import List, Optional, Deque
from collections import deque
from .base_replacer import BaseReplacer, PageReplacementResult


class LRUReplacer(BaseReplacer):
    """LRU page replacement algorithm implementation."""
    
    def get_algorithm_name(self) -> str:
        """Get the name of the algorithm."""
        return "LRU"
        
    def replace_pages_with_frames(self, page_sequence: List[str], frames_data: List) -> PageReplacementResult:
        """
        Execute LRU page replacement algorithm with initial frame data.
        
        Args:
            page_sequence: List of page IDs to access
            frames_data: List of Frame objects with initial state
            
        Returns:
            PageReplacementResult with complete execution details
        """
        num_frames = len(frames_data)
        result = PageReplacementResult(page_sequence, num_frames)
        
        # Sort frames by load time to establish initial LRU queue order
        sorted_frames = sorted(frames_data, key=lambda f: f.load_time)
        
        # Initialize frame states with their initial pages
        frame_pages = {}  # frame_id -> current_page
        frame_queue = deque()  # Queue of frame_ids in LRU order (least recent first)
        
        for frame in sorted_frames:
            frame_pages[frame.frame_id] = frame.pages_in_memory if frame.pages_in_memory else None
            frame_queue.append(frame.frame_id)
        
        # Process each page request
        for time, page_id in enumerate(page_sequence):
            # Check if page is already in memory (page hit)
            current_pages = [frame_pages[frame.frame_id] for frame in frames_data]
            is_hit = page_id in current_pages
            
            if is_hit:
                # Page hit - find which frame contains the page and move to back
                for frame_id, current_page in frame_pages.items():
                    if current_page == page_id:
                        # Remove frame from current position and move to back
                        frame_queue.remove(frame_id)
                        frame_queue.append(frame_id)
                        break
            else:
                # Page fault - replace page in least recently used frame (front of queue)
                lru_frame_id = frame_queue.popleft()  # Remove from front (LRU)
                frame_pages[lru_frame_id] = page_id   # Replace page
                frame_queue.append(lru_frame_id)      # Move to back (most recently used)
            
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