# Data Module Design Document

**Version:** 1.0
**Scope:** Backend domain model, service layer, and data structures
**Source:** Derived from the system class diagram
**Audience:** Backend engineers implementing/maintaining the simulation engine, and frontend engineers who need to understand what shapes backend data ultimately takes before it's serialized into the REST/WebSocket contracts

---

## Table of Contents

1. [Module Overview](#1-module-overview)
2. [Layered Architecture](#2-layered-architecture)
3. [Core Domain Entities](#3-core-domain-entities)
4. [Session Layer](#4-session-layer)
5. [Process Layer](#5-process-layer)
6. [Scheduling Layer](#6-scheduling-layer)
7. [Simulation State Layer](#7-simulation-state-layer)
8. [Metrics Layer](#8-metrics-layer)
9. [Real-Time Delivery Layer](#9-real-time-delivery-layer)
10. [Class Relationship Summary](#10-class-relationship-summary)
11. [Design Patterns Used](#11-design-patterns-used)

---

## 1. Module Overview

The data module is organized around a **per-session simulation model**: every browser tab creates an isolated `SessionData` record, keyed by `sessionId`, that holds its own process list, scheduler configuration, and runtime state. No state is shared across sessions.

At a high level, requests flow:

```
Controller → SessionService / ProcessFactory / SimulationService
                                      ↓
                        SchedulerService ↔ SimulationState ↔ MetricService
                                      ↓
                            WebSocketService (pushes snapshots to client)
```

---

## 2. Layered Architecture

| Layer | Responsibility | Key Classes |
|---|---|---|
| **API / Controller** | Receives HTTP requests, delegates to services, has no business logic itself | `Controller` |
| **Session Management** | Creates/destroys isolated per-user simulation sessions | `SessionService`, `SessionData` |
| **Domain Entities** | Plain data objects representing a process and its lifecycle | `Process`, `ProcessStatus`, `ProcessFactory` |
| **Scheduling Engine** | Runs the selected scheduling algorithm and produces a timeline | `SchedulerService`, `SchedulingStrategy` (+6 concrete strategies), `ScheduleReviser` |
| **Simulation State** | Tracks per-session runtime state (schedule, clock, metrics) | `SimulationState`, `SimData`, `ScheduleSegment` |
| **Metrics Engine** | Computes performance statistics from a completed/partial schedule | `MetricService`, `MetricStrategy` (+5 concrete strategies) |
| **Real-Time Delivery** | Streams state snapshots to the frontend over WebSocket | `WebSocketService` |

---

## 3. Core Domain Entities

### 3.1 `Process`

The fundamental unit of simulation. One instance per process created by the user.

| Field | Type | Description |
|---|---|---|
| `id` | int | Unique identifier, assigned by `ProcessFactory` on creation |
| `arrival_time` | int | Tick at which the process becomes eligible for scheduling |
| `burst_time` | int | Total CPU time required to complete |
| `priority` | int | Used only by `PriorityNonPreemptive` / `PriorityPreemptive` strategies |
| `remaining_time` | int | CPU time still owed; decremented as the schedule progresses |
| `status` | `ProcessStatus` | Current lifecycle state (see below) |
| `start_time` | int | Tick of first CPU allocation (used for response time) |
| `completion_time` | int | Tick at which the process finished |
| `color` | string | Hex color assigned for consistent UI/Gantt rendering |

Exposes standard getters/setters; otherwise a plain data holder with no business logic — all mutation is driven externally by `SchedulerService` / `ScheduleReviser`.

### 3.2 `ProcessStatus` (enum)

```
WAITING   → process has not yet arrived
READY     → arrived, sitting in the ready queue
RUNNING   → currently allocated to the CPU
COMPLETED → finished execution
```

### 3.3 `ProcessFactory`

Stateless factory responsible for turning raw incoming JSON (from `POST /processes` or bulk import) into validated `Process` instances.

| Method | Signature | Description |
|---|---|---|
| `createProcesses` | `(jsonList) → List<Process>` | Validates and instantiates one or more processes, assigning sequential IDs and default status `WAITING` |

---

## 4. Session Layer

### 4.1 `SessionService`

| Method | Signature | Description |
|---|---|---|
| `createSession` | `() → sessionId` | Generates a new UUID and initializes an empty `SessionData` record |
| `endSession` | `(sessionId) → void` | Tears down all state associated with a session (process list, scheduler config, simulation state, WebSocket connection) |

### 4.2 `SessionData`

The root aggregate for a single user's simulation. Held in `Controller.sessionMap`, keyed by `sessionId`.

| Field | Type | Description |
|---|---|---|
| `processList` | `List<Process>` | All processes currently defined for this session |
| `algorithm` | string | Currently selected scheduling algorithm |
| `timeQuantum` | int | Time quantum, relevant only when `algorithm == ROUND_ROBIN` |
| `action` | string | Last simulation control action received (`play`, `pause`, `step`, etc.) |
| `speed` | int | Playback speed multiplier (`1`, `2`, or `5`) |

### 4.3 `Controller`

The single entry point for all inbound API calls. Holds no simulation logic — purely orchestrates calls into the service layer and maintains the `sessionMap`.

| Field | Type | Description |
|---|---|---|
| `sessionMap` | `Map<sessionId, SessionData>` | In-memory registry of all active sessions |
| `sessionService` | `SessionService` | Delegate for session lifecycle |
| `processFactory` | `ProcessFactory` | Delegate for process creation/validation |
| `simulationService` | `SimulationService` | Delegate for scheduling + real-time delivery |

| Method | Signature | Maps to REST endpoint |
|---|---|---|
| `createSession` | `(json) → sessionId` | `POST /session` |
| `addProcess` | `(sessionId, json) → Process` | `POST /processes` |
| `editProcess` | `(sessionId, pid, json) → void` | `PUT /processes/{id}` |
| `deleteProcess` | `(sessionId, pid) → void` | `DELETE /processes/{id}` |
| `updateScheduler` | `(sessionId, algo, tq) → void` | `PUT /scheduler` |
| `handleAction` | `(sessionId, action, speed) → void` | `POST /simulation/{play\|pause\|resume\|reset\|step\|previous\|forward}`, `PUT /simulation/speed` |

---

## 5. Process Layer

Process mutation always flows through `Controller → ProcessFactory` (on create) or directly against `SessionData.processList` (on edit/delete), and any structural change triggers `SchedulerService.recompute` so the schedule stays consistent with the current process set.

```
addProcess(sessionId, json)
  → processFactory.createProcesses([json])
  → SessionData.processList.append(process)
  → schedulerService.recompute(sessionId, processList, algorithm, timeQuantum, currentTime)
```

---

## 6. Scheduling Layer

### 6.1 `SchedulerService`

Owns the scheduling computation pipeline for a session.

| Field | Type | Description |
|---|---|---|
| `strategy` | `SchedulingStrategy` | The currently active algorithm implementation, selected based on `SessionData.algorithm` |
| `simulationState` | `SimulationState` | Shared runtime state store (schedule, clock, metrics) |
| `scheduleReviser` | `ScheduleReviser` | Reconciles process objects against the current point in the schedule |

| Method | Signature | Description |
|---|---|---|
| `computeInitial` | `(sessionId, processList, algo, tq) → void` | Builds the schedule from scratch (used on session start / reset / algorithm change) |
| `recompute` | `(sessionId, processList, algo, tq, currentTime) → void` | Re-runs scheduling from `currentTime` forward (used after process add/edit/delete mid-simulation) |

### 6.2 `SchedulingStrategy` (abstract / strategy pattern)

```ts
abstract execute(processList, timeQuantum) → List<ScheduleSegment>
```

Six concrete implementations, one per supported algorithm:

| Strategy Class | Algorithm | Preemptive? | Uses `timeQuantum`? |
|---|---|---|---|
| `FCFS` | First Come First Serve | No | No |
| `SJFNonPreemptive` | Shortest Job First | No | No |
| `SJFPreemptive` | Shortest Remaining Time First | Yes | No |
| `PriorityNonPreemptive` | Priority Scheduling | No | No |
| `PriorityPreemptive` | Priority Scheduling | Yes | No |
| `RoundRobin` | Round Robin | Yes | Yes |

`SchedulerService.strategy` is swapped at runtime based on `SessionData.algorithm` — a textbook **Strategy pattern**, allowing new algorithms to be added without touching `SchedulerService` itself.

### 6.3 `ScheduleReviser`

| Method | Signature | Description |
|---|---|---|
| `reconcile` | `(simulationState, processList, currentTime) → List<Process>` | Walks the computed `ScheduleSegment` list up to `currentTime` and updates each `Process`'s `status`, `remaining_time`, `start_time`, and `completion_time` accordingly — this is what produces the live `Process[]` snapshot pushed over WebSocket |

### 6.4 `ScheduleSegment`

The atomic output unit of any `SchedulingStrategy` — equivalent to one bar in the Gantt chart.

| Field | Type | Description |
|---|---|---|
| `process` | `Process` | The process occupying the CPU during this segment (or `null`/idle marker) |
| `start` | int | Tick at which this segment begins |
| `end` | int | Tick at which this segment ends |

---

## 7. Simulation State Layer

### 7.1 `SimulationState`

Central runtime store, keyed by session, sitting between the scheduling engine and the metrics/delivery layers.

| Field | Type | Description |
|---|---|---|
| `dataMap` | `Map<sessionId, SimData>` | Per-session runtime state |
| `metricService` | `MetricService` | Delegate for computing performance metrics |

| Method | Signature | Description |
|---|---|---|
| `getSchedule` / `setSchedule` | `(sessionId[, segments])` | Read/write the full `ScheduleSegment` list |
| `appendSchedule` | `(sessionId, segments)` | Extends the schedule (e.g. after a `recompute`) without discarding history |
| `getCurrentTime` / `setCurrentTime` | `(sessionId[, t])` | Read/write the simulation clock — advanced by `step`/`play`, rewound by `previous` |
| `getMetrics` / `setMetrics` | `(sessionId[, m])` | Read/write the cached `MetricsResult` |

### 7.2 `SimData`

The concrete per-session state record held inside `SimulationState.dataMap`.

| Field | Type | Description |
|---|---|---|
| `schedule` | `List<ScheduleSegment>` | Full computed timeline for this session |
| `currentTime` | int | Current simulation tick |
| `metrics` | `MetricsResult` | Last computed metrics snapshot |
| `processList` | `List<Process>` | Current process states (mirrors `SessionData.processList` post-reconciliation) |

---

## 8. Metrics Layer

### 8.1 `MetricService`

| Field | Type | Description |
|---|---|---|
| `strategies` | `List<MetricStrategy>` | All registered metric calculators, run together to build one `MetricsResult` |

| Method | Signature | Description |
|---|---|---|
| `computeMetrics` | `(schedule, processList) → MetricsResult` | Runs every registered `MetricStrategy` and aggregates results |

### 8.2 `MetricStrategy` (abstract / strategy pattern)

```ts
abstract calculate(schedule, processList) → PartialMetricResult
```

Five concrete implementations, mirroring the metrics exposed via `GET /metrics`:

| Strategy Class | Produces |
|---|---|
| `WaitingTimeStrategy` | `waiting_time` (per-process + average) |
| `TurnaroundTimeStrategy` | `turnaround_time` (per-process + average) |
| `ResponseTimeStrategy` | `response_time` (per-process + average) |
| `CompletionTimeStrategy` | `completion_time` (per-process) |
| `CPUUtilizationStrategy` | `cpu_utilization` (percentage) |

Adding a new metric means adding a new `MetricStrategy` implementation — `MetricService` requires no changes.

---

## 9. Real-Time Delivery Layer

### 9.1 `WebSocketService`

| Field | Type | Description |
|---|---|---|
| `simulationState` | `SimulationState` | Read access to the live per-session runtime state used to build outgoing snapshot messages |

| Method | Signature | Description |
|---|---|---|
| `openConnection` | `(sessionId) → void` | Registers a new WebSocket client for a session |
| `closeConnection` | `(sessionId) → void` | Deregisters the client (on tab close / session end) |
| `handleAction` | `(sessionId, action, speed) → void` | Receives simulation control commands (`play`, `pause`, `step`, etc.), drives the tick loop, and pushes resulting `PROCESS_TABLE` / `READY_QUEUE` / `RUNNING_PROCESS` / `COMPLETED_QUEUE` / `CPU_STATE` / `GANTT_CHART` / `PERFORMANCE_METRICS` messages |
| `getCurrentDeliveryTime` | `(sessionId) → currentTime` | Returns the tick currently reflected in the last pushed snapshot, used to avoid duplicate/out-of-order pushes |

---

## 10. Class Relationship Summary

```
Controller
 ├─ owns → SessionService
 ├─ owns → ProcessFactory
 ├─ owns → SimulationService
 └─ maintains → Map<sessionId, SessionData>
                    └─ contains → List<Process> → ProcessStatus

SimulationService
 ├─ owns → SchedulerService
 │           ├─ owns → SchedulingStrategy (FCFS | SJF | SJF-P | Priority | Priority-P | RR)
 │           ├─ owns → SimulationState
 │           │           ├─ owns → MetricService → MetricStrategy (×5)
 │           │           └─ maintains → Map<sessionId, SimData>
 │           │                             └─ contains → List<ScheduleSegment>, List<Process>
 │           └─ owns → ScheduleReviser
 └─ owns → WebSocketService → reads → SimulationState
```

**Cardinality notes:**
- `Controller` : `SessionData` = 1 : many (one per active session)
- `SchedulerService` : `SchedulingStrategy` = 1 : 1 at any given time (strategy swapped per session's `algorithm`)
- `MetricService` : `MetricStrategy` = 1 : many (all strategies run every time)
- `SimulationState` : `SimData` = 1 : many (one per active session)

---

## 11. Design Patterns Used

| Pattern | Where | Why |
|---|---|---|
| **Strategy** | `SchedulingStrategy` (6 algorithms), `MetricStrategy` (5 metrics) | Swap scheduling algorithm or add new metrics without modifying the calling service |
| **Factory** | `ProcessFactory` | Centralizes validation and ID assignment when creating processes |
| **Repository / Registry** | `Controller.sessionMap`, `SimulationState.dataMap` | Keyed in-memory storage of per-session state, isolating one user's simulation from another's |
| **Facade** | `SimulationService` | Presents a single simplified interface (`handleAction`) over the more complex `SchedulerService` + `WebSocketService` collaboration |
| **Observer-like push** | `WebSocketService` | Backend-driven state push to frontend on every tick, rather than frontend polling |
