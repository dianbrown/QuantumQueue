"""
Resource Path Helper for PyInstaller

This module provides a helper function to get the correct path to resources
whether running in development mode or as a PyInstaller bundle.
"""

import sys
import os
import json
from typing import Any, Optional


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


def load_json_resource(relative_path: str, default: Optional[dict] = None) -> Any:
    """Load a JSON resource from disk in both dev and PyInstaller builds.

    Args:
        relative_path: Path relative to project root / PyInstaller MEIPASS,
            e.g. 'tutorial_kb/fcfs_steps.json'.
        default: Value to return if the file can't be opened/parsed.

    Returns:
        Parsed JSON (typically dict/list) or `default`.
    """
    path = resource_path(relative_path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {} if default is None else default
