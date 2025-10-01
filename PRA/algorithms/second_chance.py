"""Second Chance (Clock) page replacement algorithm."""

from typing import List, Optional, Dict
from collections import deque
from .base_replacer import BaseReplacer, PageReplacementResult


class SecondChanceReplacer(BaseReplacer):
    """Second Chance page replacement algorithm implementation."""
    
    def get_algorithm_name(self) -> str:
        """Get the name of the algorithm."""
        return "Second Chance"
        
    def replace_pages_with_frames(self, page_sequence: List[str], frames_data: List) -> PageReplacementResult:
        """
        Execute Second Chance page replacement algorithm with initial frame data.
        
        Args:
            page_sequence: List of page IDs to access
            frames_data: List of Frame objects with initial state
            
        Returns:
            PageReplacementResult with complete execution details
        """
        num_frames = len(frames_data)
        result = PageReplacementResult(page_sequence, num_frames)
        
        # Sort frames by load time to establish initial FIFO queue order
        sorted_frames = sorted(frames_data, key=lambda f: f.load_time)
        
        # Initialize frame states with their initial pages
        frame_pages = {}  # frame_id -> current_page
        frame_queue = deque()  # Queue of frame_ids in FIFO order
        r_bits = {}  # frame_id -> R-bit value (1 = has second chance, 0 = no second chance)
        
        for frame in sorted_frames:
            frame_pages[frame.frame_id] = frame.pages_in_memory if frame.pages_in_memory else None
            frame_queue.append(frame.frame_id)
            r_bits[frame.frame_id] = 1  # Initial R-bit value = 1
        
        # Process each page request
        for time, page_id in enumerate(page_sequence):
            # Check if page is already in memory (page hit)
            current_pages = [frame_pages[frame.frame_id] for frame in frames_data]
            is_hit = page_id in current_pages
            
            if is_hit:
                # Page hit - find the frame and set its R-bit to 1
                for frame_id, current_page in frame_pages.items():
                    if current_page == page_id:
                        r_bits[frame_id] = 1  # Give page a second chance
                        break
                # List order remains unchanged
            else:
                # Page fault - find victim using Second Chance algorithm
                self.handle_page_fault(frame_pages, frame_queue, r_bits, page_id)
            
            # Record the access result with current frame state (in original order)
            current_state = [frame_pages[frame.frame_id] for frame in frames_data]
            result.add_access(page_id, time, is_hit, current_state)
            
        return result
    
    def handle_page_fault(self, frame_pages: dict, frame_queue: deque, r_bits: dict, new_page: str):
        """
        Handle a page fault using Second Chance algorithm.
        
        Args:
            frame_pages: Current frame -> page mapping
            frame_queue: Queue of frame IDs in FIFO order
            r_bits: R-bit values for each frame
            new_page: New page to load
        """
        # Check if all R-bits are 1
        all_r_bits_one = all(r_bits[fid] == 1 for fid in frame_queue)
        
        if all_r_bits_one:
            # When all R-bits are 1, set them all to 0 without changing list order
            for fid in frame_queue:
                r_bits[fid] = 0
        
        # Find victim frame using Second Chance logic
        victim_found = False
        while not victim_found:
            # Look at first frame in queue (oldest)
            candidate_frame_id = frame_queue[0]
            
            if r_bits[candidate_frame_id] == 0:
                # R-bit is 0, this page is the victim
                victim_frame_id = frame_queue.popleft()  # Remove from front
                frame_pages[victim_frame_id] = new_page   # Load new page
                frame_queue.append(victim_frame_id)       # Add to back
                r_bits[victim_frame_id] = 1               # Set R-bit to 1
                victim_found = True
            else:
                # R-bit is 1, give it a second chance
                frame_id = frame_queue.popleft()  # Remove from front
                r_bits[frame_id] = 0              # Change R-bit to 0
                frame_queue.append(frame_id)      # Move to back
                # Continue to next frame
        
    def replace_pages(self, page_sequence: List[str], num_frames: int) -> PageReplacementResult:
        """
        Legacy method for backward compatibility.
        """
        # Create dummy frames for compatibility
        from ..models.frame import Frame
        frames_data = [Frame(str(i), i, "") for i in range(num_frames)]
        return self.replace_pages_with_frames(page_sequence, frames_data)
