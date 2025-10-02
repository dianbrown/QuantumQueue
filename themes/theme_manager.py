"""
Theme Manager for the CPU Scheduling Application
Handles loading and applying themes from JSON configuration files
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any


class ThemeManager:
    """Manages application themes loaded from JSON files"""
    
    def __init__(self):
        self.themes_dir = Path(__file__).parent
        self.themes = {}
        self.load_all_themes()
    
    def load_all_themes(self):
        """Load all theme files from the themes directory"""
        theme_files = self.themes_dir.glob("*.json")
        
        for theme_file in theme_files:
            try:
                with open(theme_file, 'r', encoding='utf-8-sig') as f:
                    theme_data = json.load(f)
                    theme_name = theme_data.get('name', theme_file.stem)
                    self.themes[theme_name] = theme_data
            except Exception as e:
                print(f"Error loading theme {theme_file}: {e}")
    
    def get_available_themes(self) -> List[str]:
        """Get list of available theme names"""
        return list(self.themes.keys())
    
    def get_theme(self, theme_name: str) -> Dict[str, Any]:
        """Get theme configuration by name"""
        return self.themes.get(theme_name, {})
    
    def get_theme_colors(self, theme_name: str) -> Dict[str, str]:
        """Get color palette for a specific theme"""
        theme = self.get_theme(theme_name)
        return theme.get('colors', {})
    
    def theme_exists(self, theme_name: str) -> bool:
        """Check if a theme exists"""
        return theme_name in self.themes
    
    def reload_themes(self):
        """Reload all themes from files"""
        self.themes.clear()
        self.load_all_themes()
