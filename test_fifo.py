"""Test the FIFO algorithm with the user's specific example."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'PRA'))

from PRA.algorithms.fifo import FIFOReplacer
from PRA.models.frame import Frame


def test_fifo_algorithm():
    """Test FIFO with the specific example provided by user."""
    
    # Create frames with initial pages and load times
    frames_data = [
        Frame("0", 11, "5"),  # Frame 0: Load time 11, Page 5
        Frame("1", 8, "8"),   # Frame 1: Load time 8, Page 8  
        Frame("2", 3, "1"),   # Frame 2: Load time 3, Page 1
        Frame("3", 14, "4"),  # Frame 3: Load time 14, Page 4
    ]
    
    # Page sequence to process
    page_sequence = ["9", "7", "8", "3", "5", "7", "7", "9", "6", "3", "3"]
    
    # Create FIFO algorithm instance
    fifo = FIFOReplacer()
    
    # Run the algorithm
    result = fifo.replace_pages_with_frames(page_sequence, frames_data)
    
    print("FIFO Algorithm Test Results:")
    print("=" * 50)
    print(f"Initial frame state (sorted by load time):")
    sorted_frames = sorted(frames_data, key=lambda f: f.load_time)
    for i, frame in enumerate(sorted_frames):
        print(f"  Frame {frame.frame_id}: Load time {frame.load_time}, Page {frame.pages_in_memory}")
    
    print(f"\nQueue order (by load time): {[f.frame_id for f in sorted_frames]}")
    print(f"Page sequence: {page_sequence}")
    print("\nStep-by-step execution:")
    print("-" * 50)
    
    for i, access in enumerate(result.accesses):
        status = "HIT" if access.is_hit else "FAULT"
        print(f"Step {i+1}: Page {access.page_id} -> {status}")
        print(f"  Frame state: {access.frame_state}")
        if not access.is_hit:
            print(f"  -> Page fault! Replaced in oldest frame")
        print()
    
    print(f"Total Page Faults: {result.get_page_faults()}")
    print(f"Total Page Hits: {result.get_page_hits()}")
    

if __name__ == "__main__":
    test_fifo_algorithm()
