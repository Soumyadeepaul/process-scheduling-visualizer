# Contributing Guide

## Project Overview

The **Process Scheduling Visualizer** is an interactive web application that demonstrates how different CPU scheduling algorithms work through real-time simulation and visualization.

The application is intended as both a learning tool and a practical demonstration of operating system scheduling concepts.

### Tech Stack

- **Frontend:** React.js
- **Backend:** FastAPI
- **Communication:** REST APIs + WebSockets
- **Project Management:** Jira
- **Version Control:** Git & GitHub

---

## Initial Features

The first version of the project will support:

- Add Processes
- Select CPU Scheduling Algorithm
- Switch Scheduling Algorithm at any time
- Start, Pause, Resume and Reset Simulation
- Control Simulation Speed (x1, x2, x5)
- Step-by-Step Execution
- Real-time Process State Visualization
- Dynamic Ready Queue Visualization
- Gantt Chart Generation
- Scheduling Metrics
  - Waiting Time
  - Turnaround Time
  - Response Time
  - Completion Time
  - CPU Utilization
- Process Arrival & Burst Time Configuration
- Algorithm-specific Parameters (e.g. Time Quantum for Round Robin)

---

## Planned Scheduling Algorithms

- FCFS
- SJF (Non-Preemptive)
- SJF (Preemptive)
- Priority (Non-Preemptive)
- Priority (Preemptive)
- Round Robin

---

# Development Workflow

We follow the workflow:

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
3. Create a feature branch using the Jira issue key.
4. Implement the assigned task.
5. Commit changes using the Jira issue key.
6. Push the branch.
7. Create a Pull Request.
8. After approval, merge into `main`.
9. Move the Jira issue to **Done**.

---

# Branch Naming Convention

```
feature/KAN-8-lld-design
feature/KAN-9-api-websocket
feature/KAN-10-frontend-architecture
feature/KAN-11-domain-models

bugfix/KAN-22-fcfs-calculation
docs/KAN-15-contributing-guide
refactor/KAN-18-scheduler-service
```

Format:

```
<type>/<JIRA-ID>-short-description
```

### Branch Types

- feature
- bugfix
- hotfix
- docs
- refactor
- chore

---

# Creating a Branch

Update your local repository first.

```bash
git checkout main
git pull origin main
```

Create a branch for the Jira issue.

```bash
git checkout -b feature/KAN-9-api-websocket
```

---

# Commit Message Convention

Every commit should begin with the Jira issue key.

Examples:

```text
KAN-8: Design scheduler LLD

KAN-9: Implement WebSocket communication

KAN-10: Create scheduler dashboard

KAN-11: Add process domain models

KAN-17: Fix Round Robin execution logic
```

Format:

```text
<JIRA-ID>: Short meaningful description
```

Keep commits focused on a single logical change.

---

# VS Code Workflow

1. Open the project in VS Code.
2. Fetch the latest changes.
3. Checkout your feature branch.
4. Complete the assigned Jira task.
5. Test your changes locally.
6. Commit using the required naming convention.
7. Push the branch.
8. Open a Pull Request.

---

# General Guidelines

- One Jira issue = One feature branch.
- Keep commits small and meaningful.
- Pull the latest `main` before starting new work.
- Do not commit secrets, API keys or `.env` files.
- Ensure the project builds successfully before pushing.
- Every change should be reviewed through a Pull Request before merging.

---