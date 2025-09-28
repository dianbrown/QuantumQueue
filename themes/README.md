# Themes Folder

This folder contains theme configuration files for the CPU Scheduling Application.

## How to Create a Custom Theme

1. Create a new `.json` file in this folder with your theme name (e.g., `mytheme.json`)
2. Follow the JSON structure shown in the existing theme files
3. Restart the application to see your new theme in the Settings panel

## Theme File Structure

```json
{
    "name": "Your Theme Name",
    "description": "Description of your theme",
    "author": "Your Name",
    "version": "1.0.0",
    "colors": {
        "main_bg": "#color",           // Main window background
        "sidebar_bg": "#color",        // Sidebar background
        "sidebar_header_bg": "#color", // Sidebar header background
        "sidebar_border": "#color",    // Sidebar borders
        "sidebar_hover": "#color",     // Sidebar button hover color
        "sidebar_active": "#color",    // Active sidebar button color
        "sidebar_accent": "#color",    // Sidebar accent color (border)
        "text_primary": "#color",      // Primary text color
        "text_secondary": "#color",    // Secondary text color
        "button_bg": "#color",         // Button background
        "button_hover": "#color",      // Button hover color
        "input_bg": "#color",          // Input field background
        "input_border": "#color",      // Input field border
        "table_bg": "#color",          // Table background
        "table_grid": "#color",        // Table grid lines
        "header_bg": "#color"          // Table header background
    }
}
```

## Color Format

Use hex color codes (e.g., `#ff6b35`) for all color values.

## Available Themes

- **dark_default.json** - The default dark theme
- **light.json** - Clean light theme
- **blue.json** - Deep blue theme
- **green.json** - Forest green theme
- **purple.json** - Royal purple theme
- **sunset.json** - Example custom theme with warm colors

## Theme Manager

The `theme_manager.py` file handles loading and managing themes. It automatically:
- Loads all `.json` files from this folder
- Makes them available in the Settings panel
- Provides fallback handling for missing themes
