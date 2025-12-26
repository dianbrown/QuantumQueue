"""
SJF Tutorial Page - Step-by-step walkthrough of Shortest Job First algorithm
Non-preemptive scheduling with shortest burst time selection
"""

import json
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                              QLabel, QTableWidget, QTableWidgetItem, QFrame,
                              QScrollArea, QHeaderView)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont

from CPU.utils.process_generator import ProcessGenerator

# Resource helper (PyInstaller-safe)
from resource_path import load_json_resource


class SJFTutorialPage(QWidget):
    """Step-by-step SJF algorithm tutorial page with dynamic step generation"""
    
    back_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_step = 0
        self.current_theme = {}
        self.scheduling_block_color = QColor("#ffff00")
        self.processes = []
        self.steps = []
        self._updating_table = False
        self.step_templates = self._load_step_templates()
        
        self.setup_ui()
        self._generate_random_processes()
        self._populate_process_table()
        self._setup_timeline_grid()
        self._generate_steps()
        self._show_step(0)
    
    def _load_step_templates(self):
        """Load step description templates from JSON file"""
        templates = load_json_resource('tutorial_kb/sjf_steps.json', default=None)
        if isinstance(templates, dict) and templates.get('step_types'):
            return templates
        return self._get_default_templates()
    
    def _get_default_templates(self):
        return {
            "step_types": {
                "initial": {"title": "Step 0: Initial State", "description": "SJF selects shortest burst first."},
                "show_arrivals": {"title": "Step 1: Mark Arrivals", "description": "RS markers shown."},
                "first_block": {"title": "Step {step}: Process {process_id} begins", "description": "Shortest burst starts."},
                "continue_block": {"title": "Step {step}: Process {process_id} continues", "description": "Continues."},
                "process_complete": {"title": "Step {step}: Process {process_id} completes", "description": "Complete."},
                "final": {"title": "Step {step}: Final Solution", "description": "Complete!"}
            }
        }
    
    def _generate_random_processes(self):
        generated = ProcessGenerator.generate_processes(num_processes=4, unique_arrivals=False)
        self.processes = [{"id": p.id, "priority": p.priority, "arrival": p.arrival, "burst": p.burst} for p in generated]
    
    def _get_processes_from_table(self):
        self.processes = []
        for row in range(4):
            try:
                pid = self.timeline_grid.item(row, 0).text() if self.timeline_grid.item(row, 0) else chr(ord('A') + row)
                priority = int(self.timeline_grid.item(row, 1).text()) if self.timeline_grid.item(row, 1) else 1
                arrival = int(self.timeline_grid.item(row, 2).text()) if self.timeline_grid.item(row, 2) else 1
                burst = int(self.timeline_grid.item(row, 3).text()) if self.timeline_grid.item(row, 3) else 1
                self.processes.append({"id": pid, "priority": max(1,min(10,priority)), "arrival": max(1,min(30,arrival)), "burst": max(1,min(15,burst))})
            except:
                self.processes.append({"id": chr(ord('A')+row), "priority": 1, "arrival": 1, "burst": 3})
    
    def _on_table_cell_changed(self, row, column):
        if self._updating_table or column < 1 or column > 3:
            return
        self._get_processes_from_table()
        self._generate_steps()
        self.current_step = 0
        self._setup_timeline_grid()
        self._show_step(0)
    
    def _generate_steps(self):
        """Generate tutorial steps for SJF (non-preemptive, shortest burst first)"""
        self.steps = []
        templates = self.step_templates.get("step_types", {})
        
        process_map = {p['id']: p.copy() for p in self.processes}
        for pid in process_map:
            process_map[pid]['remaining'] = process_map[pid]['burst']
            process_map[pid]['completed'] = False
        
        process_list = ", ".join([f"{p['id']}(B={p['burst']})" for p in self.processes])
        arrival_order = " → ".join([f"{p['id']} at t={p['arrival']}" for p in sorted(self.processes, key=lambda x: (x['arrival'], x['id']))])
        rs_markers = {p['id']: [p['arrival']] for p in self.processes}
        
        # Step 0: Initial
        initial = templates.get("initial", {})
        self.steps.append({
            "title": initial.get("title", "Step 0"),
            "description": initial.get("description", "").format(num_processes=len(self.processes), process_list=process_list),
            "timeline": {}, "rs_markers": {}
        })
        
        # Step 1: Show RS
        arrivals = templates.get("show_arrivals", {})
        self.steps.append({
            "title": arrivals.get("title", "Step 1"),
            "description": arrivals.get("description", "").format(arrival_order=arrival_order),
            "timeline": {}, "rs_markers": {k: v.copy() for k, v in rs_markers.items()}
        })
        
        # Simulate SJF
        step_num = 2
        current_time = 1
        timeline = {}
        start_times = {}
        end_times = {}
        execution_order = []
        
        while current_time <= 32:
            # Get ready processes
            ready = [p for p in process_map.values() if p['arrival'] <= current_time and not p['completed'] and p['remaining'] > 0]
            
            if not ready:
                # Check if any process left
                remaining_procs = [p for p in process_map.values() if not p['completed']]
                if not remaining_procs:
                    break
                current_time += 1
                continue
            
            # Sort by burst, arrival, id (SJF)
            ready.sort(key=lambda p: (p['burst'], p['arrival'], p['id']))
            current_process = ready[0]
            pid = current_process['id']
            burst = current_process['burst']
            arrival = current_process['arrival']
            
            if pid not in start_times:
                start_times[pid] = current_time
                execution_order.append(pid)
            
            # Ready list for description
            ready_list = ", ".join([f"{p['id']}(B={p['burst']})" for p in ready])
            
            # Execute all blocks for this process (non-preemptive)
            for block_num in range(1, burst + 1):
                if pid not in timeline:
                    timeline[pid] = []
                timeline[pid].append(current_time)
                
                remaining = burst - block_num
                is_first = (block_num == 1)
                is_last = (block_num == burst)
                
                if is_first:
                    tmpl = templates.get("first_block", {})
                    title = tmpl.get("title", "").format(step=step_num, process_id=pid, burst=burst)
                    desc = tmpl.get("description", "").format(
                        step=step_num, process_id=pid, burst=burst, current_time=current_time, ready_list=ready_list
                    )
                elif is_last:
                    end_time = current_time + 1
                    end_times[pid] = end_time
                    tat = end_time - arrival
                    wait = start_times[pid] - arrival
                    tmpl = templates.get("process_complete", {})
                    title = tmpl.get("title", "").format(step=step_num, process_id=pid)
                    desc = tmpl.get("description", "").format(
                        step=step_num, process_id=pid, burst=burst, start_time=start_times[pid],
                        end_time=end_time, wait_time=wait, tat=tat
                    )
                else:
                    tmpl = templates.get("continue_block", {})
                    title = tmpl.get("title", "").format(step=step_num, process_id=pid, current_time=current_time)
                    desc = tmpl.get("description", "").format(
                        step=step_num, process_id=pid, burst=burst, block_num=block_num, remaining=remaining, current_time=current_time
                    )
                
                self.steps.append({
                    "title": title, "description": desc,
                    "timeline": {k: v.copy() for k, v in timeline.items()},
                    "rs_markers": {k: v.copy() for k, v in rs_markers.items()}
                })
                step_num += 1
                current_time += 1
            
            process_map[pid]['remaining'] = 0
            process_map[pid]['completed'] = True
            end_times[pid] = current_time
        
        # Final step
        exec_order_str = " → ".join(execution_order)
        metrics_lines = []
        total_wait = total_tat = 0
        for proc in self.processes:
            pid = proc['id']
            start = start_times.get(pid, 0)
            end = end_times.get(pid, 0)
            tat = end - proc['arrival'] if end else 0
            wait = start - proc['arrival'] if start else 0
            total_wait += wait
            total_tat += tat
            metrics_lines.append(f"- {pid}: Burst={proc['burst']}, WT={wait}, TAT={tat}")
        
        final = templates.get("final", {})
        self.steps.append({
            "title": final.get("title", "Final").format(step=step_num),
            "description": final.get("description", "").format(
                step=step_num, execution_order=exec_order_str, metrics="\n".join(metrics_lines),
                avg_wait=f"{total_wait/len(self.processes):.2f}", avg_tat=f"{total_tat/len(self.processes):.2f}"
            ),
            "timeline": {k: v.copy() for k, v in timeline.items()},
            "rs_markers": {k: v.copy() for k, v in rs_markers.items()}
        })
        
        if hasattr(self, 'step_indicator'):
            self.step_indicator.setText(f"Step 0 of {len(self.steps) - 1}")
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        top_layout = QHBoxLayout()
        self.back_btn = QPushButton("Back to Help")
        self.back_btn.setObjectName("backBtn")
        self.back_btn.setMaximumWidth(150)
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.clicked.connect(self.back_requested.emit)
        top_layout.addWidget(self.back_btn)
        top_layout.addStretch()
        
        self.random_btn = QPushButton("Generate Random")
        self.random_btn.setObjectName("randomBtn")
        self.random_btn.setCursor(Qt.PointingHandCursor)
        self.random_btn.clicked.connect(self._on_random_clicked)
        top_layout.addWidget(self.random_btn)
        layout.addLayout(top_layout)
        
        self.page_title = QLabel("SJF Tutorial")
        self.page_title.setObjectName("tutorialTitle")
        layout.addWidget(self.page_title)
        
        self.timeline_grid = QTableWidget(4, 36)
        headers = ["Process ID", "Priority", "Arrival", "Burst"] + [str(i) for i in range(1, 33)]
        self.timeline_grid.setHorizontalHeaderLabels(headers)
        self.timeline_grid.setColumnWidth(0, 70)
        self.timeline_grid.setColumnWidth(1, 55)
        self.timeline_grid.setColumnWidth(2, 55)
        self.timeline_grid.setColumnWidth(3, 45)
        for i in range(4, 36):
            self.timeline_grid.setColumnWidth(i, 35)
        self.timeline_grid.verticalHeader().setDefaultSectionSize(30)
        self.timeline_grid.verticalHeader().hide()
        self.timeline_grid.cellChanged.connect(self._on_table_cell_changed)
        self._setup_timeline_grid()
        layout.addWidget(self.timeline_grid)
        
        step_frame = QFrame()
        step_frame.setObjectName("stepFrame")
        step_layout = QVBoxLayout(step_frame)
        step_layout.setSpacing(5)
        step_layout.setContentsMargins(15, 15, 15, 15)
        self.step_title = QLabel("Step 0: Initial State")
        self.step_title.setObjectName("stepTitle")
        step_layout.addWidget(self.step_title)
        
        desc_scroll = QScrollArea()
        desc_scroll.setWidgetResizable(True)
        desc_scroll.setMinimumHeight(120)
        desc_scroll.setMaximumHeight(200)
        desc_scroll.setObjectName("descriptionScroll")
        self.step_description = QLabel("")
        self.step_description.setObjectName("stepDescription")
        self.step_description.setWordWrap(True)
        self.step_description.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        desc_scroll.setWidget(self.step_description)
        step_layout.addWidget(desc_scroll)
        step_layout.addStretch(0)  # Prevent expansion
        layout.addWidget(step_frame)
        
        nav_layout = QHBoxLayout()
        nav_layout.addStretch()
        self.prev_btn = QPushButton("Previous")
        self.prev_btn.setObjectName("navBtn")
        self.prev_btn.setCursor(Qt.PointingHandCursor)
        self.prev_btn.clicked.connect(self._prev_step)
        nav_layout.addWidget(self.prev_btn)
        
        self.step_indicator = QLabel("Step 0 of 6")
        self.step_indicator.setObjectName("stepIndicator")
        nav_layout.addWidget(self.step_indicator)
        
        self.next_btn = QPushButton("Next")
        self.next_btn.setObjectName("navBtn")
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.clicked.connect(self._next_step)
        nav_layout.addWidget(self.next_btn)
        nav_layout.addStretch()
        layout.addLayout(nav_layout)
    
    def _populate_process_table(self):
        self._updating_table = True
        for i, proc in enumerate(self.processes):
            id_item = QTableWidgetItem(proc["id"])
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            id_item.setTextAlignment(Qt.AlignCenter)
            self.timeline_grid.setItem(i, 0, id_item)
            for j, key in enumerate(["priority", "arrival", "burst"], 1):
                item = QTableWidgetItem(str(proc[key]))
                item.setTextAlignment(Qt.AlignCenter)
                self.timeline_grid.setItem(i, j, item)
        self._updating_table = False
    
    def _on_random_clicked(self):
        self._generate_random_processes()
        self._populate_process_table()
        self._generate_steps()
        self.current_step = 0
        self._setup_timeline_grid()
        self._show_step(0)
    
    def _setup_timeline_grid(self):
        self._updating_table = True
        for i in range(4):
            for j in range(4, 36):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(Qt.white)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.timeline_grid.setItem(i, j, item)
        self._updating_table = False
    
    def _show_step(self, step_index):
        if step_index < 0 or step_index >= len(self.steps):
            return
        self.current_step = step_index
        step = self.steps[step_index]
        self.step_title.setText(step["title"])
        self.step_description.setText(step["description"])
        self.step_indicator.setText(f"Step {step_index} of {len(self.steps) - 1}")
        self.prev_btn.setEnabled(step_index > 0)
        self.next_btn.setEnabled(step_index < len(self.steps) - 1)
        self._update_timeline(step["timeline"], step["rs_markers"])
    
    def _update_timeline(self, timeline_data, rs_markers):
        if not self.timeline_grid:
            return
        process_to_row = {proc["id"]: i for i, proc in enumerate(self.processes[:4])}
        for row in range(4):
            for col in range(4, 36):
                item = self.timeline_grid.item(row, col)
                if item:
                    item.setBackground(Qt.white)
                    item.setText("")
                    item.setForeground(QColor(0, 0, 0))
        for pid, times in timeline_data.items():
            row = process_to_row.get(pid)
            if row is not None:
                for t in times:
                    if 1 <= t <= 32:
                        col = t + 3
                        item = self.timeline_grid.item(row, col)
                        if item:
                            item.setBackground(self.scheduling_block_color)
                            item.setText("-")
        for pid, times in rs_markers.items():
            row = process_to_row.get(pid)
            if row is not None:
                for t in times:
                    if 1 <= t <= 32:
                        col = t + 3
                        item = self.timeline_grid.item(row, col)
                        if item:
                            txt = item.text()
                            item.setText(f"{txt}\nRS" if txt else "RS")
                            item.setForeground(QColor(128, 128, 128))
    
    def _next_step(self):
        self._show_step(self.current_step + 1)
    
    def _prev_step(self):
        self._show_step(self.current_step - 1)
    
    def reset_tutorial(self):
        self._show_step(0)
    
    def showEvent(self, event):
        super().showEvent(event)
        if self.current_step < len(self.steps):
            self._update_timeline(self.steps[self.current_step]["timeline"], self.steps[self.current_step]["rs_markers"])
    
    def apply_theme(self, theme: dict):
        self.current_theme = theme
        if 'scheduling_block_bg' in theme:
            self.scheduling_block_color = QColor(theme['scheduling_block_bg'])
        
        text_color = theme.get('text_primary', '#ffffff')
        text_secondary = theme.get('text_secondary', '#c3c3c3')
        button_bg = theme.get('button_bg', '#7289da')
        button_hover = theme.get('button_hover', '#677bc4')
        input_bg = theme.get('input_bg', '#40444b')
        table_bg = theme.get('table_bg', '#40444b')
        table_grid = theme.get('table_grid', '#72767d')
        header_bg = theme.get('header_bg', '#2c2f33')
        
        self.setStyleSheet(f"""
            QWidget {{ background-color: {theme.get('main_bg', '#36393f')}; color: {text_color}; }}
            QLabel#tutorialTitle {{ font-size: 28px; font-weight: bold; color: {button_bg}; background-color: transparent; }}
            QPushButton#randomBtn {{ background-color: {input_bg}; border: 1px solid {table_grid}; padding: 10px 20px; border-radius: 6px; color: {text_color}; font-size: 14px; }}
            QPushButton#randomBtn:hover {{ background-color: {theme.get('sidebar_hover', '#4a4f56')}; border: 1px solid {button_bg}; }}
            QLabel#stepTitle {{ font-size: 20px; font-weight: bold; color: {text_color}; background-color: transparent; }}
            QLabel#stepDescription {{ font-size: 14px; color: {text_color}; background-color: transparent; padding: 10px; }}
            QLabel#stepIndicator {{ font-size: 14px; color: {text_secondary}; background-color: transparent; margin: 0 20px; }}
            QFrame#stepFrame {{ background-color: {input_bg}; border: 1px solid {table_grid}; border-radius: 8px; padding: 15px; }}
            QScrollArea#descriptionScroll {{ border: none; background-color: transparent; }}
            QPushButton#backBtn {{ background-color: {input_bg}; border: none; padding: 10px 20px; border-radius: 6px; color: {text_color}; font-size: 14px; }}
            QPushButton#backBtn:hover {{ background-color: {theme.get('sidebar_hover', '#4a4f56')}; }}
            QPushButton#navBtn {{ background-color: {button_bg}; border: none; padding: 10px 30px; border-radius: 6px; color: {theme.get('button_text', '#ffffff')}; font-size: 14px; font-weight: bold; }}
            QPushButton#navBtn:hover {{ background-color: {button_hover}; }}
            QPushButton#navBtn:disabled {{ background-color: {input_bg}; color: {text_secondary}; }}
            QTableWidget {{ background-color: {table_bg}; gridline-color: {table_grid}; border: 1px solid {table_grid}; color: {text_color}; }}
            QTableWidget::item {{ padding: 5px; }}
            QHeaderView::section {{ background-color: {header_bg}; color: {text_color}; padding: 5px; border: 1px solid {table_grid}; }}
        """)
        if self.current_step < len(self.steps):
            self._update_timeline(self.steps[self.current_step]["timeline"], self.steps[self.current_step]["rs_markers"])
