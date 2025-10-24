"""Clock Page Replacement Algorithm implementation."""

from typing import List, Dict, Optional
from .base_replacer import BaseReplacer, PageReplacementResult


class ClockReplacer(BaseReplacer):
    """
    Clock Page Replacement Algorithm.
    
    Similar to Second Chance but cycles through frames in order based on load time.
    - Order determined by LOAD TIME column (remains in this order)
    - No FIFO queue like Second Chance
    - Initial R-bit value = 1
    - Initial pointer location is the frame with oldest page
    
    On PAGE FAULT:
    - Page in oldest frame (pointed to) is removed
    - That frame's R-bit is set to 1
    - Pointer moves to next oldest frame
    - Special case: If all R-bits are 1, set all to 0 first
    
    On PAGE HIT:
    - R-bit of the frame containing the page is set to 1
    - Pointer remains at current position
    """
    
    def get_algorithm_name(self) -> str:
        """Get the name of the algorithm."""
        return "Clock"
    
    def replace_pages_with_frames(self, page_sequence: List[str], frames_data: List) -> PageReplacementResult:
        """
        Execute Clock page replacement algorithm with initial frame data.
        
        Args:
            page_sequence: List of page IDs to access
            frames_data: List of Frame objects with initial state
            
        Returns:
            PageReplacementResult with complete execution details
        """
        num_frames = len(frames_data)
        result = PageReplacementResult(page_sequence, num_frames)
        
        # Clock order: Start with highest frame, then wrap to lowest and go up
        # For frames [4,3,2,1,0], clock order should be: 4 -> 0 -> 1 -> 2 -> 3 -> 4 -> ...
        frame_ids_sorted = sorted([f.frame_id for f in frames_data], reverse=True)
        if frame_ids_sorted:
            # Start with highest, then add rest in ascending order
            highest = frame_ids_sorted[0]
            rest = sorted([f for f in frame_ids_sorted if f != highest])
            frame_order = [highest] + rest
        else:
            frame_order = [f.frame_id for f in frames_data]
        
        # Initialize frame states with their initial pages
        frame_pages = {}  # frame_id -> current_page
        for frame in frames_data:
            frame_pages[frame.frame_id] = frame.pages_in_memory if frame.pages_in_memory else None
        
        # Initialize R-bits to 1 for all frames
        r_bits = {f.frame_id: 1 for f in frames_data}
        
        # Pointer starts at the frame with the LOWEST load time (oldest page)
        oldest_frame = min(frames_data, key=lambda f: f.load_time)
        pointer_index = frame_order.index(oldest_frame.frame_id)
        
        # Track if this is the first fault (need to reset R-bits)
        first_fault = True
        
        # Process each page request
        for time, page_id in enumerate(page_sequence):
            # Check if page is already in memory (page hit)
            current_pages = [frame_pages[frame.frame_id] for frame in frames_data]
            is_hit = page_id in current_pages
            
            if is_hit:
                # PAGE HIT
                # Find the frame containing the page and set its R-bit to 1
                for frame_id, current_page in frame_pages.items():
                    if current_page == page_id:
                        r_bits[frame_id] = 1
                        break
                
                # Pointer remains at current position (no change)
                
                # Record the state
                result.add_access(page_id, time, True, current_pages)
                
            else:
                # PAGE FAULT - Clock Algorithm
                
                # Check if all R-bits are 1 (or first fault)
                if first_fault or all(rbit == 1 for rbit in r_bits.values()):
                    # Reset all R-bits to 0 BEFORE the fault
                    r_bits = {frame_id: 0 for frame_id in r_bits}
                    first_fault = False
                    
                    # Victim is directly at pointer (all R-bits are 0 now)
                    victim_index = pointer_index
                else:
                    # Normal case: Sweep to find victim
                    # Start at pointer and sweep forward
                    victim_index = pointer_index
                    
                    # While current frame has R-bit = 1, set to 0 and move forward
                    while r_bits[frame_order[victim_index]] == 1:
                        r_bits[frame_order[victim_index]] = 0
                        victim_index = (victim_index + 1) % len(frame_order)
                    
                    # Now victim_index points to frame with R-bit = 0
                
                # Get the victim frame
                victim_frame_id = frame_order[victim_index]
                
                # Replace the page
                frame_pages[victim_frame_id] = page_id
                
                # Set the new page's R-bit to 1
                r_bits[victim_frame_id] = 1
                
                # Move the clock hand forward to next frame
                pointer_index = (victim_index + 1) % len(frame_order)
                
                # Record the state
                current_pages = [frame_pages[frame.frame_id] for frame in frames_data]
                result.add_access(page_id, time, False, current_pages)
        
        return result
    
    def replace_pages(self, page_sequence: List[str], num_frames: int) -> PageReplacementResult:
        """
        Legacy method for backward compatibility.
        """
        # Create dummy frames for compatibility
        from ..models.frame import Frame
        frames_data = [Frame(str(i), i, "") for i in range(num_frames)]
        return self.replace_pages_with_frames(page_sequence, frames_data)
    
    def find_victim_frame(self, frame_order: List[str], start_index: int, rbit_states: Dict[str, int]) -> str:
        """
        Find the victim frame using clock algorithm.
        
        Starts at current pointer position and cycles through frames.
        First frame with R-bit = 0 is selected as victim.
        Frames with R-bit = 1 are skipped (and their R-bit is set to 0).
        
        Args:
            frame_order: List of frame IDs in clock order
            start_index: Current pointer position
            rbit_states: Dictionary of R-bit states
            
        Returns:
            Frame ID of victim frame
        """
        num_frames = len(frame_order)
        index = start_index
        
        # Cycle through frames until we find one with R-bit = 0
        while True:
            frame_id = frame_order[index]
            
            if rbit_states[frame_id] == 0:
                # Found victim - frame with R-bit = 0
                return frame_id
            else:
                # R-bit is 1, give it a second chance
                rbit_states[frame_id] = 0
                # Move to next frame in clock order
                index = (index + 1) % num_frames
