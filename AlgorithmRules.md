# Algorithm Rules Reference

This document defines the concrete implementation rules for all CPU Scheduling and Page Replacement algorithms in this application. These rules can be used as a reference for implementing these algorithms in any application.

---

# CPU Scheduling Algorithms

## Common Definitions

| Term | Definition |
|------|------------|
| **Burst Time** | Total CPU time required by a process |
| **Arrival Time** | Time when process enters the ready queue |
| **Priority** | Higher number = higher priority (preempts lower) |
| **Waiting Time** | Turnaround Time - Burst Time |
| **Turnaround Time** | End Time - Arrival Time |
| **Ready State (RS)** | Time when process becomes eligible for selection in Round Robin |
| **Timeline** | Array where index `i` represents time unit `i+1` (1-indexed grid) |

---

## 1. FCFS (First Come First Served)

### Core Rules
1. **Non-preemptive** – once a process starts, it runs to completion
2. **Selection criteria**: Process with earliest arrival time
3. **Tie-breaker**: Process ID (alphabetical/numerical order)

### Algorithm Steps
```
1. Sort all processes by (arrival_time, process_id)
2. Set current_time = 1
3. For each process in sorted order:
   a. If current_time < process.arrival → advance to arrival
   b. Execute process for entire burst duration
   c. current_time += burst
```

### Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty process list | Return empty result |
| Process arrives later | Idle time until process arrives |
| Same arrival time | Select by process ID order |
| Process burst exceeds timeline (32) | Truncate at timeline boundary |

---

## 2. SJF (Shortest Job First)

### Core Rules
1. **Non-preemptive** – once a process starts, it runs to completion
2. **Selection criteria**: Process with shortest burst time from ready queue
3. **Tie-breakers** (in order):
   - Shortest burst time
   - Earliest arrival time
   - Process ID

### Algorithm Steps
```
1. Set current_time = 1
2. While processes remain:
   a. Add all arrived processes to ready_queue
   b. Sort ready_queue by (burst, arrival, id)
   c. Select first process, run to completion
   d. If no ready process → advance time
```

### Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty process list | Return empty result |
| No process ready at current time | Advance time by 1 |
| Multiple processes with same burst | Pick earliest arrival |
| Same burst + same arrival | Pick by process ID |

---

## 3. SRT (Shortest Remaining Time)

### Core Rules
1. **Preemptive** – process can be interrupted by shorter remaining time
2. **Selection criteria**: Process with shortest **remaining** burst time
3. **Preemption trigger**: New process arrives with shorter remaining burst
4. **Tie-breakers** (in order):
   - Shortest remaining burst
   - Earliest arrival time
   - Process ID

### Algorithm Steps
```
1. Set current_time = 1, current_process = None
2. While processes remain:
   a. Add all arrived processes to ready_queue
   b. Check if new process has shorter burst → preempt current
   c. If no current_process → select from ready_queue by (remaining_burst, arrival, id)
   d. Execute current_process for 1 time unit
   e. If burst depleted → mark complete
```

### Edge Cases
| Scenario | Handling |
|----------|----------|
| New process has EQUAL remaining time | No preemption (current continues) |
| New process has SHORTER remaining time | Preempt current, add to ready queue |
| Process resumes after preemption | First execution time is start_time |
| Multiple arrivals at same time | All added, then best selected |

---

## 4. FCFS with Priority (Preemptive)

### Core Rules
1. **Preemptive** – higher priority preempts lower priority
2. **Priority interpretation**: Higher number = higher priority (configurable)
3. **Within same priority**: FCFS ordering by Ready State time
4. **Tie-breakers** (in order):
   - Priority (higher first)
   - Ready State time (earlier first)
   - Process ID

### Algorithm Steps
```
1. Set current_time = 1, current_process = None
2. While processes remain:
   a. Add arrived processes, record ready_state_time = current_time
   b. If new process.priority > current_process.priority → preempt
   c. Sort ready_queue by (-priority, ready_state_time, id)
   d. Execute current_process for 1 time unit
```

### Edge Cases
| Scenario | Handling |
|----------|----------|
| New process has SAME priority | No preemption (follow FCFS) |
| Preempted process re-enters | Gets new ready_state_time = preemption time |
| Multiple high-priority arrivals | Sorted by ready_state_time among them |
| `higher_is_better = False` | Lower number = higher priority |

---

## 5. SJF with Priority (Preemptive)

### Core Rules
1. **Preemptive** – higher priority OR shorter burst can preempt
2. **Selection criteria**: Priority first, then original burst time
3. **Preemption trigger**: 
   - New process has higher priority, OR
   - Same priority but shorter **original** burst time
4. **Tie-breakers** (in order):
   - Priority (descending)
   - Original burst time (ascending)
   - Arrival time
   - Process ID

### Algorithm Steps
```
1. Set current_time = 1, current_process = None
2. Store original_burst for each process
3. While processes remain:
   a. Add arrived processes to ready_queue
   b. Check preemption: new.priority > current.priority OR 
      (same priority AND new.original_burst < current.original_burst)
   c. Sort ready_queue by (-priority, original_burst, arrival, id)
   d. Execute for 1 time unit
```

### Edge Cases
| Scenario | Handling |
|----------|----------|
| Same priority, same original burst | Use arrival time, then ID |
| Uses ORIGINAL burst, not remaining | Comparison always against initial burst |
| Remaining burst decreases | Original burst stays constant for comparison |

---

## 6. Round Robin

### Core Rules
1. **Preemptive by quantum** – process yields after time quantum expires
2. **No priority preemption** – only quantum expiration causes switch
3. **Ready State (RS)** tracking:
   - Initial RS = arrival time
   - After quantum expires: RS = time when quantum ended
4. **Selection criteria**: Earliest Ready State time
5. **Tie-breaker for RS**: Newest arrival (most recent arrival first)

### Algorithm Steps
```
1. Set current_time = 1, quantum = Q (default 2)
2. Each process gets ready_state = arrival_time
3. While processes remain:
   a. Add arrived processes to ready_queue
   b. Sort ready_queue by (ready_state, -arrival)  # newest arrival wins ties
   c. Execute for min(quantum, remaining_burst)
   d. If burst remains: new ready_state = current_time, add to queue
```

### Edge Cases
| Scenario | Handling |
|----------|----------|
| Process finishes before quantum | Completes early, no re-queue |
| Quantum expires with work left | Process re-queued with new RS |
| Same RS time | Pick process with most recent arrival |
| New arrival during execution | Added to queue, no preemption mid-quantum |

---

## 7. Round Robin with Priority

### Core Rules
1. **Preemptive by priority** AND **by quantum**
2. **Higher priority preempts immediately** (even mid-quantum)
3. **Same priority**: Regular Round Robin rules apply (RS-based, quantum-limited)
4. **Ready State (RS)** tracking same as Round Robin
5. **Selection criteria**:
   - Highest priority first
   - Among same priority: earliest Ready State
   - Tie-breaker: newest arrival

### Algorithm Steps
```
1. Set current_time = 1, quantum = Q
2. While processes remain:
   a. Add arrived processes
   b. Check if new process.priority > current.priority → preempt immediately
   c. Get highest priority processes
   d. Among them, sort by (ready_state, -arrival)
   e. Execute for 1 time unit, track quantum
   f. If quantum expires: update RS, move to queue
```

### Edge Cases
| Scenario | Handling |
|----------|----------|
| Higher priority arrives mid-quantum | Immediate preemption, preempted process gets new RS |
| Same priority arrives | No preemption, added to queue |
| Preempted process resumes | Continues with remaining burst, fresh quantum |
| Multiple highest priority | Use RS time and arrival among them |

---

## Metrics Calculation (All Algorithms)

```python
turnaround_time = end_time - arrival_time
waiting_time = turnaround_time - original_burst_time
waiting_time = max(0, waiting_time)  # Ensure non-negative

average_waiting = sum(waiting_times) / num_processes
average_turnaround = sum(turnaround_times) / num_processes
```

---

# Page Replacement Algorithms (PRA)

## Common Definitions

| Term | Definition |
|------|------------|
| **Frame** | Memory slot that can hold one page |
| **Page Hit** | Requested page is already in memory |
| **Page Fault** | Requested page not in memory, replacement needed |
| **Load Time** | Initial time when page was loaded into frame |
| **R-bit** | Reference bit (1 = recently used, 0 = not recently used) |
| **Victim** | Frame selected for page replacement |

---

## 1. FIFO (First In, First Out)

### Core Rules
1. **Replace oldest page** (first one loaded)
2. **Queue order**: Determined by load time on initialization
3. **On page fault**: Front of queue is victim, new page goes to back
4. **On page hit**: No change to queue order

### Algorithm Steps
```
1. Sort frames by load_time to establish queue order
2. Initialize frame_queue as deque
3. For each page request:
   a. If page in memory → HIT (no action)
   b. If page fault:
      - victim_frame = queue.popleft()  # oldest
      - frame[victim] = new_page
      - queue.append(victim)  # move to back
```

### Edge Cases
| Scenario | Handling |
|----------|----------|
| Page hit | Queue order unchanged |
| Empty frame | Treated same as fault (fill first) |
| Same load time | Use frame ID order |

---

## 2. LRU (Least Recently Used)

### Core Rules
1. **Replace least recently USED page** (not loaded)
2. **Initial queue order**: By load time (oldest first)
3. **On page hit**: Move accessed frame to back (most recent)
4. **On page fault**: Front of queue is victim (LRU)

### Algorithm Steps
```
1. Sort frames by load_time for initial LRU order
2. Initialize frame_queue as deque
3. For each page request:
   a. If page in memory → HIT:
      - Find frame containing page
      - Remove from queue, append to back (MRU position)
   b. If page fault:
      - victim_frame = queue.popleft()  # LRU
      - frame[victim] = new_page
      - queue.append(victim)  # now MRU
```

### Edge Cases
| Scenario | Handling |
|----------|----------|
| Page hit | Frame moves to back of queue |
| Multiple hits same page | Each hit refreshes position |
| Which page is LRU | Front of queue after all updates |

---

## 3. Optimal (OPT / Farthest in Future)

### Core Rules
1. **Replace page used farthest in future**
2. **Perfect knowledge required** – needs entire page sequence
3. **If page never used again**: Highest priority for replacement
4. **Tie-breaker**: Lowest frame number (frame ID)

### Algorithm Steps
```
1. Initialize frames with initial pages
2. For each page request at time t:
   a. If page in memory → HIT
   b. If page fault:
      - For each page in memory:
        - Find next occurrence in sequence[t+1:]
        - If never used again → distance = infinity
      - Select frame with maximum distance
      - If tie → lowest frame number
      - Replace victim with new page
```

### Edge Cases
| Scenario | Handling |
|----------|----------|
| Page never used again | Distance = infinity (highest priority victim) |
| Multiple pages never used again | Choose lowest frame number |
| Same future distance | Choose lowest frame number |
| Page hit | No change to frames |

---

## 4. Second Chance (Enhanced FIFO)

### Core Rules
1. **FIFO with R-bit check**
2. **Initial R-bit = 1** for all frames
3. **On page hit**: Set R-bit = 1 for that frame
4. **On page fault**:
   - If ALL R-bits are 1: Clear all to 0 first
   - Examine front of queue:
     - If R-bit = 0: Select as victim
     - If R-bit = 1: Set to 0, move to back, continue
5. **After replacement**: New page's R-bit = 1

### Algorithm Steps
```
1. Sort frames by load_time for FIFO queue
2. Initialize all R-bits = 1
3. For each page request:
   a. If page in memory → HIT:
      - Set R-bit[found_frame] = 1
   b. If page fault:
      - If all R-bits == 1: Set all to 0
      - While front.R-bit == 1:
          front.R-bit = 0
          Move front to back
      - victim = front (R-bit = 0)
      - Replace page, set R-bit = 1, move to back
```

### Edge Cases
| Scenario | Handling |
|----------|----------|
| All R-bits are 1 | Reset ALL to 0, then first in queue is victim |
| Page hit | Only R-bit update, no queue change |
| Frame gets second chance | Moves to back with R-bit = 0 |
| Frame used again before eviction | R-bit reset to 1 on hit |

---

## 5. Clock (Circular Buffer)

### Core Rules
1. **Fixed circular order** – frames don't move, pointer sweeps
2. **Order**: Highest frame first, then ascending (e.g., 4→0→1→2→3→4...)
3. **Initial pointer**: Points to frame with oldest load time
4. **Initial R-bit = 1** for all frames
5. **On page hit**: Set R-bit = 1, pointer stays
6. **On page fault**:
   - If ALL R-bits are 1: Reset all to 0, victim is at pointer
   - Else: Sweep until R-bit = 0, clearing R-bits along the way
   - Replace page, set R-bit = 1, advance pointer

### Algorithm Steps
```
1. Create frame_order: [highest, then ascending]
   Example: [4, 0, 1, 2, 3]
2. Pointer starts at frame with lowest load_time
3. Initialize all R-bits = 1
4. For each page request:
   a. If page in memory → HIT:
      - R-bit[frame] = 1
      - Pointer unchanged
   b. If page fault:
      - If first fault OR all R-bits == 1:
          Reset all R-bits to 0
          victim = frame_order[pointer]
      - Else:
          While R-bit[pointer] == 1:
              R-bit[pointer] = 0
              pointer = (pointer + 1) % num_frames
          victim = frame_order[pointer]
      - Replace page, R-bit[victim] = 1
      - pointer = (pointer + 1) % num_frames
```

### Edge Cases
| Scenario | Handling |
|----------|----------|
| First page fault | Reset all R-bits to 0, then select at pointer |
| All R-bits are 1 | Reset ALL to 0, victim is at current pointer |
| Page hit | Only R-bit update, pointer unchanged |
| Pointer wraps around | Circular: index = (index + 1) % num_frames |

---

## Metrics Calculation (All PRA)

```python
page_faults = count of all page_fault events
page_hits = count of all page_hit events

hit_ratio = page_hits / total_accesses
fault_ratio = page_faults / total_accesses
```

---

# Quick Reference: Algorithm Comparison

## CPU Scheduling

| Algorithm | Preemptive | Selection Criteria | Primary Tie-breaker |
|-----------|------------|-------------------|---------------------|
| FCFS | No | Arrival Time | Process ID |
| SJF | No | Shortest Burst | Arrival, then ID |
| SRT | Yes (shorter burst) | Shortest Remaining | Arrival, then ID |
| FCFS Priority | Yes (higher priority) | Priority → Ready State | Ready State, then ID |
| SJF Priority | Yes (priority or burst) | Priority → Original Burst | Arrival, then ID |
| Round Robin | Yes (quantum only) | Ready State Time | Newest Arrival |
| RR Priority | Yes (priority + quantum) | Priority → Ready State | Newest Arrival |

## Page Replacement

| Algorithm | Selection Strategy | R-bit Used | Order Type |
|-----------|-------------------|------------|------------|
| FIFO | First loaded (oldest) | No | Queue |
| LRU | Least recently used | No | Queue (dynamic) |
| Optimal | Farthest future use | No | Static |
| Second Chance | FIFO + second chance | Yes | Queue |
| Clock | Circular sweep | Yes | Fixed circular |

---

# Implementation Notes

## Timeline Handling
- Timeline is 1-indexed in UI display (time 1 to 32)
- Array is 0-indexed internally: `timeline[i]` represents time `i+1`
- Maximum timeline length: 32 units

## Process/Frame Initialization
- Processes created with: `(id, priority, arrival, burst)`
- Frames created with: `(frame_id, load_time, pages_in_memory)`

## Priority Convention
- **CPU Scheduling**: Higher number = Higher priority (default)
- **Configurable**: `higher_is_better` flag in FCFS Priority

## Original vs Remaining Burst
- **SJF/FCFS**: Uses actual burst time
- **SRT**: Uses remaining burst for preemption check
- **SJF Priority**: Uses **original** burst for comparison (not remaining)