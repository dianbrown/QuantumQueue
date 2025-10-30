# Changelog

All notable changes to QuantumQueue will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2025-10-30

### Fixed
- Fixed FCFS with Priority algorithm to use ready state time instead of arrival time for tie-breaking when priorities are equal
  - Processes with same priority now correctly execute in order of when they entered the ready queue (FCFS)
  - Fixes incorrect scheduling order for preempted processes with equal priority

## [1.1.0] - 2025-10-24

### Fixed
- Fixed Clock Page Replacement Algorithm implementation
  - Corrected initial R-bit values (now start at 1 instead of 0)
  - Fixed frame order cycle (highest frame → 0 → 1 → 2 → ... → highest)
  - Fixed pointer starting position (now starts at frame with lowest load time)
  - Corrected sweep behavior during page faults
  - Updated tutorial documentation to reflect correct algorithm behavior
  - Fixed simulation code in help page

## [1.0.0] - 2025-10-16

### Added
- Initial release of QuantumQueue
- CPU Scheduling algorithms:
  - First Come First Served (FCFS)
  - FCFS with Priority
  - Shortest Job First (SJF)
  - SJF with Priority
  - Shortest Remaining Time (SRT)
  - Round Robin (RR)
  - Round Robin with Priority
- Page Replacement algorithms:
  - First In First Out (FIFO)
  - Least Recently Used (LRU)
  - Optimal Page Replacement
  - Second Chance
  - Clock Algorithm
- Interactive practice mode with process/frame tables
- Gantt chart visualization for CPU scheduling
- Step-by-step tutorials for all algorithms
- Multiple theme support (28 themes including Dracula, Nord, Tokyo Night, etc.)
- Custom title bar with minimize/maximize/close controls
- Collapsible sidebar navigation
- Random process/page sequence generation
- Drag-and-drop frame blocks for PRA visualization
- Settings page with theme customization
- Desktop installers for Windows and macOS

### Features
- Modern, dark-themed UI inspired by PyDracula
- Real-time algorithm simulation
- Interactive Gantt charts with color-coded processes
- Process metrics display (waiting time, turnaround time, completion time)
- Page fault statistics and hit ratio calculation
- Algorithm comparison mode
- Customizable quantum values for Round Robin
- Frame management with load time tracking
- Visual feedback for page hits and faults

### Technical
- Built with PySide6 (Qt for Python)
- Clean architecture with separated concerns
- Modular algorithm implementations
- Theme system with JSON-based theme files
- Cross-platform support (Windows, macOS)

## [Unreleased]

### Planned
- Linux AppImage support
- Export results to PDF/Image
- Save/Load practice sessions
- Keyboard shortcuts
- Multi-language support

---

## Release Notes Format

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security fixes
