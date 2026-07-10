# High-Level Architecture (HLD)

## System Architecture

```text
                   +---------------------+
                   |        User         |
                   +----------+----------+
                              |
                              ▼
                   +---------------------+
                   |   React Frontend    |
                   +----------+----------+
                              |
                    REST API / WebSocket
                              |
                              ▼
        +------------------------------------------------+
        |              FastAPI Backend                   |
        |------------------------------------------------|
        | Controller Layer                               |
        |                                                |
        | • Session Service                              |
        | • Simulation Service                           |
        | • Scheduler Service                            |
        | • Metrics Service                              |
        | • WebSocket Service                            |
        | • Simulation State (RAM)                       |
        +--------------------+---------------------------+
                             |
                             ▼
                 +----------------------------+
                 | Scheduling Algorithms      |
                 |----------------------------|
                 | FCFS                       |
                 | SJF (NP / P)               |
                 | Priority (NP / P)          |
                 | Round Robin                |
                 +----------------------------+
```

---

# Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| **Controller Layer** | Receives all client requests and routes them to the appropriate service. |
| **Session Service** | Creates and manages isolated simulation sessions for each user. |
| **Simulation Service** | Coordinates the simulation lifecycle and controls execution (play, pause, resume, reset, step). |
| **Scheduler Service** | Executes the selected scheduling algorithm for every simulation tick. |
| **Metrics Service** | Calculates waiting time, turnaround time, response time, completion time, and CPU utilization. |
| **WebSocket Service** | Sends live simulation updates to the frontend. |
| **Simulation State (RAM)** | Stores the current simulation state for each active session in memory. |
| **Scheduling Algorithms** | Implements FCFS, SJF, Priority, and Round Robin scheduling logic. |

---

# Service Communication Flow

### 1. Create Session

```text
User
   │
   ▼
Controller Layer
   │
   ▼
Session Service
   │
Creates Session ID
   │
Stores Session in RAM
```

---

### 2. Simulation Execution

```text
User (Play / Pause / Step)
            │
            ▼
     Controller Layer
            │
            ▼
   Simulation Service
            │
            ▼
   Scheduler Service
            │
            ▼
Scheduling Algorithm
            │
Returns Updated State
            │
            ▼
Simulation State (RAM)
```

---

### 3. Metrics Generation

```text
Simulation State
        │
        ▼
Metrics Service
        │
Calculates Metrics
        │
        ▼
Simulation State
```

---

### 4. Live Frontend Updates

```text
Simulation State
        │
        ▼
WebSocket Service
        │
Pushes Live Updates
        │
        ▼
React Frontend
```

---

# Overall Data Flow

```text
User
   │
   ▼
React Frontend
   │
REST API / WebSocket
   │
   ▼
Controller Layer
   │
   ├────────► Session Service
   │
   ├────────► Simulation Service
   │               │
   │               ▼
   │       Scheduler Service
   │               │
   │               ▼
   │     Scheduling Algorithms
   │               │
   │               ▼
   │      Simulation State (RAM)
   │               │
   ├────────► Metrics Service
   │               │
   └────────► WebSocket Service
                   │
                   ▼
            React Frontend
```

## Communication Summary

| Sender | Receiver | Purpose |
|---------|----------|---------|
| React Frontend | Controller Layer | Send REST/WebSocket requests. |
| Controller Layer | Session Service | Create and manage sessions. |
| Controller Layer | Simulation Service | Execute simulation commands. |
| Simulation Service | Scheduler Service | Advance the simulation by one tick. |
| Scheduler Service | Scheduling Algorithms | Execute the selected scheduling logic. |
| Scheduling Algorithms | Simulation State (RAM) | Update process states and queues. |
| Simulation State | Metrics Service | Provide data for metric calculation. |
| Metrics Service | Simulation State | Store updated metrics. |
| Simulation State | WebSocket Service | Provide the latest simulation state. |
| WebSocket Service | React Frontend | Push real-time updates to the user. |