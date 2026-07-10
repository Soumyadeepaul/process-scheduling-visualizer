# Contributing Guide

## Project Overview

The **Process Scheduling Virtualizer (PSV)** is an interactive web application that demonstrates and visualizes CPU scheduling algorithms through real-time simulation.

Unlike a traditional scheduling calculator, PSV acts as a **real-time virtualizer** where users can create processes, modify scheduling parameters, switch algorithms while the simulation is running, and observe how processes transition between different scheduling states.

The backend is the **single source of truth** for the simulation, while the frontend is responsible for providing a smooth, real-time visualization of the scheduler.

---

# Tech Stack

- **Frontend:** React.js
- **Backend:** FastAPI
- **Communication:** REST APIs + WebSockets
- **Project Management:** Jira
- **Version Control:** Git & GitHub

---

# Initial Features

The first release will include the following functionality.

## Process Management

- Add Processes
- Edit Processes
- Delete Processes
- Configure Arrival Time
- Configure Burst Time
- Configure Priority (when applicable)

---

## Scheduling

- Select Scheduling Algorithm
- Switch Algorithm at any time
- Support algorithm-specific parameters
- Preserve simulation state while changing algorithms

---

## Simulation Controls

- Play
- Pause
- Resume
- Reset
- Step Execution
- Go Back (Previous Simulation State)
- Fast Forward
- Simulation Speed Control (1×, 2×, 5×)

---

## Visualization

- Live Process Table
- Ready Queue Visualization
- Running Process Visualization
- Terminated Queue Visualization
- Smooth Process State Animations
- Live Gantt Chart
- Current CPU State
- Real-time Scheduler Updates using WebSockets

---

## Metrics

Users can generate metrics at any point during the simulation.

Metrics include:

- Waiting Time
- Turnaround Time
- Response Time
- Completion Time
- CPU Utilization

---

# Planned Scheduling Algorithms

- FCFS
- SJF (Non-Preemptive)
- SJF (Preemptive)
- Priority (Non-Preemptive)
- Priority (Preemptive)
- Round Robin

Future versions may include additional scheduling algorithms.

---

# High-Level Architecture

The backend owns the complete simulation.

The frontend never performs scheduling calculations. It only renders the simulation state received from the backend.

```
                React Frontend
                       │
        REST API + WebSocket Communication
                       │
                FastAPI Backend
                       │
             Simulation Controller
                       │
      ┌───────────────┼───────────────┐
      │               │               │
Scheduler      Metrics Engine   Session Manager
      │
Simulation State
      │
WebSocket Publisher
```

The **Simulation Controller** acts as the single source of truth for every user's simulation.

---

# User Session Flow

When a user opens the application:

```
Browser
    │
GET /session
    │
    ▼
Backend generates Session ID
    │
    ▼
Browser stores Session ID
(Session Storage)
```

Every subsequent request contains the Session ID.

```
{
    session_id,
    request_data
}
```

The backend retrieves the user's simulation using this Session ID and either updates the existing state or creates a new one if necessary.

This enables multiple users to run completely independent simulations simultaneously.

---

# Simulation Flow

```
User Action
     │
     ▼
REST API Request
     │
     ▼
Simulation Controller
     │
     ▼
Scheduler
     │
     ▼
Update Simulation State
     │
     ▼
Calculate Metrics
     │
     ▼
Broadcast Snapshot
     │
     ▼
WebSocket
     │
     ▼
Frontend Visualization
```

Every simulation update originates from the backend.

---


# API Design

The backend follows a **REST + WebSocket** architecture.

- **REST APIs** are responsible for creating, updating, deleting and controlling the simulation.
- **WebSockets** are responsible for broadcasting real-time simulation updates to the frontend.

Every REST request (except session creation) must include the user's **Session ID**.

---

## Session APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/session` | Create a new user session and return a Session ID |

The frontend stores the returned Session ID in **Session Storage** and includes it in all future requests.

---

## Process APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/process` | Add a new process |
| PUT | `/process/{pid}` | Update a process |
| DELETE | `/process/{pid}` | Delete a process |
| GET | `/processes` | Get all processes |

---

## Scheduler APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/scheduler/algorithm` | Change scheduling algorithm |
| GET | `/scheduler/algorithms` | Get supported algorithms |

---

## Simulation APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/simulation/play` | Start simulation |
| POST | `/simulation/pause` | Pause simulation |
| POST | `/simulation/resume` | Resume simulation |
| POST | `/simulation/reset` | Reset simulation |
| POST | `/simulation/step` | Execute one simulation step |
| POST | `/simulation/back` | Move to previous simulation state |
| POST | `/simulation/speed` | Change simulation speed |

---

## Metrics APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/metrics` | Generate metrics for the current simulation state |

---

## WebSocket

```
ws://<host>/ws/{session_id}
```

The frontend establishes a WebSocket connection after obtaining a Session ID.

The backend pushes real-time simulation updates, including:

- Current Time
- Ready Queue
- Running Process
- Waiting Queue
- Terminated Queue
- Gantt Chart Updates
- Process State Changes
- Live Metrics

The frontend should **never compute scheduling logic**. It should only render the simulation state received from the backend.

---

## Request Flow

```
Frontend
     │
REST Request
(Session ID + Payload)
     │
     ▼
FastAPI
     │
     ▼
Simulation Controller
     │
     ▼
Scheduler Engine
     │
     ▼
Simulation State Updated
     │
     ▼
WebSocket Broadcast
     │
     ▼
React UI Updated
```

---

## Response Format

All REST APIs should return a consistent response structure.

```json
{
    "success": true,
    "message": "Process added successfully",
    "data": {}
}
```

Error responses should follow the same structure.

```json
{
    "success": false,
    "message": "Invalid Process ID",
    "error": {}
}
```

---

## Design Principles

- Backend is the **single source of truth**.
- Every simulation belongs to a unique Session ID.
- All simulation updates originate from the `SimulationController`.
- WebSockets are used only for broadcasting state changes.
- REST APIs are used only for user actions and state modifications.
- APIs should remain stateless except for the simulation state maintained per Session ID.

# Development Workflow

Every feature should follow the workflow below.

```
Epic
 └── Story
      └── Subtask
            └── Feature Branch
                    └── Commit
                           └── Pull Request
```

Every code change must be associated with a Jira issue.

---

# Jira Workflow

1. Pick an assigned Jira issue.
2. Move the issue to **In Progress**.
3. Create a feature branch from the Jira issue.
4. Implement the assigned work.
5. Commit using the Jira issue key.
6. Push the branch.
7. Create a Pull Request.
8. After approval, merge into `main`.
9. Move the Jira issue to **Done**.

---

# Branch Naming Convention

Use the Jira issue key in every branch name.

Examples:

```text
feature/PSV-8-session-manager

feature/PSV-9-websocket

feature/PSV-10-react-layout

feature/PSV-11-domain-models

bugfix/PSV-24-round-robin

docs/PSV-3-contributing-guide

refactor/PSV-18-scheduler-engine
```

Format

```text
<type>/<JIRA-ID>-short-description
```

## Branch Types

- feature
- bugfix
- hotfix
- docs
- refactor
- chore

---

# Creating a Branch

Update your local repository.

```bash
git checkout main
git pull origin main
```

Create a feature branch.

```bash
git checkout -b feature/PSV-9-websocket
```

---

# Commit Message Convention

Every commit should begin with the Jira issue key.

Examples

```text
PSV-8: Design simulation controller

PSV-9: Implement WebSocket communication

PSV-10: Create process table

PSV-11: Add scheduler interface

PSV-12: Add FCFS scheduler

PSV-18: Refactor simulation state
```

Format

```text
<JIRA-ID>: Short meaningful description
```

Keep commits focused on a single logical change.

---

# VS Code Workflow

1. Open the repository in VS Code.
2. Pull the latest changes from `main`.
3. Checkout your feature branch.
4. Complete the assigned Jira task.
5. Test the implementation locally.
6. Commit using the required convention.
7. Push the branch.
8. Open a Pull Request.

---

# General Guidelines

- One Jira issue should correspond to one feature branch.
- Keep commits small, meaningful, and focused.
- Pull the latest `main` before starting any new task.
- Never commit secrets, credentials, or `.env` files.
- Ensure the project builds successfully before pushing.
- Every change must be reviewed through a Pull Request before merging.
- Use meaningful branch names and commit messages.
- Keep backend logic independent from frontend rendering.
- The backend should remain the **single source of truth** for the simulation state.

---

# Development Principle

The architecture follows a clear separation of responsibilities.

- **Frontend** is responsible for user interaction and visualization.
- **Backend** is responsible for simulation, scheduling, state management, and metrics.
- **WebSocket** is responsible for synchronizing the frontend with the backend in real time.
- **Simulation Controller** is the central component responsible for maintaining and updating the simulation state.

This separation allows new scheduling algorithms and visualization features to be added with minimal changes to the overall architecture.