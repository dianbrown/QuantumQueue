"""
Resource Path Helper for PyInstaller

This module provides a helper function to get the correct path to resources
whether running in development mode or as a PyInstaller bundle.
"""

import sys
import os


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    
    When running as a PyInstaller bundle (onefile mode), files are extracted
    to a temporary folder. This function returns the correct path in both cases.
    
    Args:
        relative_path (str): Relative path to the resource (e.g., 'Assets/icons/home.png')
        
    Returns:
        str: Absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Running in development mode
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)
