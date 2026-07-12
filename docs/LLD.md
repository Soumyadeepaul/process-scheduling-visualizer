# CPU Scheduling Simulator — Design Doc

## 1. Architecture Overview

```
User → React Frontend ⇄ Controller ⇄ Session Service
                              │
                              ├──► Simulation Service ──► Scheduler Service ──► Scheduling Algorithms
                              │                                                        │
                              └──► WebSocket Service ⇄ Simulation State ⇄ Metrics Service
```

The system is a layered backend: a single **Controller** exposes REST endpoints, delegates work to focused services, and all services communicate through one shared **Simulation State** (in-memory) which the **WebSocket Service** streams to the frontend.

## 2. Modules & Responsibility

| Module | Responsibility |
|---|---|
| Controller | Entry point for all REST calls; validates requests and routes to services |
| Session Service | Creates/deletes/validates simulation sessions |
| Simulation Service | Owns simulation lifecycle (play, pause, step, reset, speed) |
| Scheduler Service | Picks and runs the active scheduling algorithm |
| Scheduling Algorithms | One algorithm each (FCFS, SJF, SJF-Preemptive, Priority, Priority-Preemptive, Round Robin) |
| Metrics Service | Computes performance metrics from simulation state |
| WebSocket Service | Pushes live state updates to the frontend |
| Simulation State | Single source of truth for the running simulation (processes, queues, CPU state, Gantt data, history) |

## 3. Design Patterns Used

| Pattern | Where | Why |
|---|---|---|
| **Facade** | Controller | Hides all internal services behind one simple API surface for the frontend |
| **Strategy** | Scheduling Algorithms (via Scheduler Service) | Swap the active scheduling algorithm at runtime without changing Scheduler Service code |
| **Strategy** | Metric Calculators (via Metrics Service) | Each metric (waiting, turnaround, response, completion, CPU utilization) is computed independently and can be added/removed without touching Metrics Service |
| **Memento**-style snapshotting | Simulation State's `history` stack | Enables step-back / previous-state playback without recomputation |
| **Observer**-style push | WebSocket Service | Frontend is notified reactively on every state change rather than polling |

## 4. When Things Get Triggered

| Trigger (user/API action) | Flow |
|---|---|
| Open app / start new run | Controller → Session Service creates a session |
| Add/update/delete a process | Controller updates Simulation State directly via Simulation Service |
| Change algorithm (dropdown) | Controller → Simulation Service → Scheduler Service `setStrategy()` |
| Press Play | Controller → Simulation Service `play()` → begins ticking |
| Each tick (auto or manual step) | Simulation Service `executeTick()` → Scheduler Service `executeStep()` → active Strategy `execute(state)` → Simulation State updated |
| Pause / Resume / Reset | Controller → Simulation Service toggles internal status, halts or reinitializes ticking |
| Step back | Simulation Service pops from `history` stack in Simulation State |
| Change speed | Controller → Simulation Service `changeSpeed()` adjusts tick interval |
| After every state change | Simulation State change → WebSocket Service `pushUpdate()` → React Frontend re-renders |
| Metrics requested (or after run completes) | Metrics Service reads Simulation State → runs each Metric Strategy → returns aggregated `Metrics` |
| Delete session / close app | Controller → Session Service `deleteSession()` |

## 5. Notes

- Controller has no direct dependency on Scheduler Service or Metrics Service — all such work is routed through Simulation Service, keeping the Controller thin.
- Simulation State is the only shared mutable object; every other service reads/writes through it rather than holding its own copy.


<p align="center">
  <img src="images/UML.png" alt="UML" width="1000"/>
</p>