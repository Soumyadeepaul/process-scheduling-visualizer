# Functional and Non-Functional Requirements

## Functional Requirements

The Process Scheduling Virtualizer (PSV) is designed as an educational platform to help users understand CPU scheduling algorithms through real-time simulation and visualization. The system should provide an interactive environment where users can create processes, control simulations, and observe scheduling decisions as they occur.

### Process Management
The application shall allow users to:
- Add new processes.
- Edit existing process information.
- Delete processes.
- Configure process attributes:
  - Arrival Time
  - Burst Time
  - Priority (where applicable)

### Scheduling
The application shall:
- Support multiple CPU scheduling algorithms.
- Allow users to select the scheduling algorithm before execution.
- Allow switching scheduling algorithms during simulation.
- Preserve the current simulation state while changing algorithms.
- Support algorithm-specific parameters (e.g., Time Quantum for Round Robin).

### Simulation Controls
Users shall be able to:
- Play simulation.
- Pause simulation.
- Resume simulation.
- Reset simulation.
- Execute one scheduling step at a time.
- Move to the previous simulation state.
- Fast-forward simulation.
- Adjust simulation speed (1×, 2×, 5×).

### Visualization
The application shall provide real-time visualization of:
- Ready Queue
- Running Process
- Completed Queue
- Current CPU State
- Live Process Table
- Live Gantt Chart
- Smooth process state transitions and animations

### Performance Metrics
The system shall calculate and display:
- Waiting Time
- Turnaround Time
- Response Time
- Completion Time
- CPU Utilization

### Session Management
To keep the application lightweight and suitable for educational use:
- Each user shall receive an independent simulation session.
- Simulation data shall remain available only for the active session.
- Session data shall be discarded when the session expires or the user disconnects.
- No user authentication or persistent storage is required in the initial release.

---

# Non-Functional Requirements

## Consistency
The backend shall act as the single source of truth for every simulation. Consistency is prioritized over availability to ensure that all simulation states remain synchronized and accurate.

**Priority**

```
Consistency > Availability
```

---

## Performance

The initial system shall be designed to support:

- Up to **10 requests per second (RPS)**.
- Request sizes ranging from **10 KB to 100 KB**.
- Peak network throughput of approximately **1 MB/s**.
- User sessions lasting up to **1 hour**.
- Approximately **3 GB** of active in-memory session data during peak usage.

Most requests involve simulation control or state retrieval, resulting in relatively low data creation compared to the total request volume.

---

## Real-Time Communication

The application shall provide low-latency communication between the frontend and backend using WebSockets. Real-time synchronization is prioritized over large-scale horizontal scalability.

The system should ensure:
- Low-latency simulation updates.
- Consistent scheduler state across all clients.
- Smooth real-time visualization.
- Immediate propagation of simulation state changes.

---

## Scalability

For the initial release (MVP), the focus is on delivering a reliable real-time simulation experience rather than supporting a large number of concurrent users. The architecture should remain modular so that distributed session management and horizontal scaling can be introduced in future versions without major architectural changes.