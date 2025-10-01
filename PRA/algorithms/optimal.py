"""Optimal (OPT/Farthest in Future) page replacement algorithm."""

from typing import List, Optional
from .base_replacer import BaseReplacer, PageReplacementResult


class OptimalReplacer(BaseReplacer):
    """Optimal page replacement algorithm implementation."""
    
    def get_algorithm_name(self) -> str:
        """Get the name of the algorithm."""
        return "Optimal"
        
    def replace_pages_with_frames(self, page_sequence: List[str], frames_data: List) -> PageReplacementResult:
        """
        Execute Optimal page replacement algorithm with initial frame data.
        
        Args:
            page_sequence: List of page IDs to access
            frames_data: List of Frame objects with initial state
            
        Returns:
            PageReplacementResult with complete execution details
        """
        num_frames = len(frames_data)
        result = PageReplacementResult(page_sequence, num_frames)
        
        # Initialize frame states with their initial pages (ignore load time for Optimal)
        frame_pages = {}  # frame_id -> current_page
        
        for frame in frames_data:
            frame_pages[frame.frame_id] = frame.pages_in_memory if frame.pages_in_memory else None
        
        # Process each page request
        for time, page_id in enumerate(page_sequence):
            # Check if page is already in memory (page hit)
            current_pages = [frame_pages[frame.frame_id] for frame in frames_data]
            is_hit = page_id in current_pages
            
            if is_hit:
                # Page hit - no replacement needed, pages in memory remain unchanged
                pass
            else:
                # Page fault - need to find optimal page to replace
                # Find which page will be used farthest in the future
                victim_frame_id = self.find_optimal_victim(
                    frame_pages, page_sequence, time + 1, frames_data
                )
                
                # Replace the page in the victim frame
                frame_pages[victim_frame_id] = page_id
            
            # Record the access result with current frame state (in original order)
            current_state = [frame_pages[frame.frame_id] for frame in frames_data]
            result.add_access(page_id, time, is_hit, current_state)
            
        return result
    
    def find_optimal_victim(self, frame_pages: dict, page_sequence: List[str], 
                           start_time: int, frames_data: List) -> str:
        """
        Find the optimal frame to replace based on future page usage.
        
        Args:
            frame_pages: Current frame -> page mapping
            page_sequence: Complete page sequence
            start_time: Current time index to look from
            frames_data: Frame data for ordering
            
        Returns:
            Frame ID of the victim frame to replace
        """
        future_distances = {}
        
        # For each frame with a page, find when that page will be needed next
        for frame_id, current_page in frame_pages.items():
            if current_page is None:
                continue
                
            # Look for the next occurrence of this page in future
            next_use_time = None
            for future_time in range(start_time, len(page_sequence)):
                if page_sequence[future_time] == current_page:
                    next_use_time = future_time
                    break
            
            if next_use_time is None:
                # Page will never be used again - highest priority for replacement
                future_distances[frame_id] = float('inf')
            else:
                # Distance to next use
                future_distances[frame_id] = next_use_time - start_time + 1
        
        # Find frame(s) with maximum distance (farthest in future)
        max_distance = max(future_distances.values())
        candidates = [fid for fid, dist in future_distances.items() if dist == max_distance]
        
        # If multiple candidates, choose the one with lowest frame number
        candidates.sort(key=lambda fid: int(fid))
        
        return candidates[0]
        
    def replace_pages(self, page_sequence: List[str], num_frames: int) -> PageReplacementResult:
        """
        Legacy method for backward compatibility.
        """
        # Create dummy frames for compatibility
        from ..models.frame import Frame
        frames_data = [Frame(str(i), i, "") for i in range(num_frames)]
        return self.replace_pages_with_frames(page_sequence, frames_data)