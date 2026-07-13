
"""
SessionData domain model.

The root aggregate for a single user's simulation, held in
Controller.session_map keyed by session_id. Holds the process list,
the selected scheduler configuration, and the last simulation control
action/speed received for that session. This is intentionally a plain
data holder: all mutation logic that has side effects on the schedule
(e.g. recompute) is triggered by the Controller/SimulationService,
not by SessionData itself.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from app.models.process import Process

DEFAULT_ALGORITHM = "FCFS"
ALLOWED_SPEEDS = (1, 2, 5)
ALLOWED_ALGORITHMS = (
    "FCFS",
    "SJF",
    "SJF_PREEMPTIVE",
    "PRIORITY",
    "PRIORITY_PREEMPTIVE",
    "ROUND_ROBIN",
)


@dataclass
class SessionData:
    """Per-session state owned directly by the Controller."""

    session_id: str
    process_list: List[Process] = field(default_factory=list)
    algorithm: str = DEFAULT_ALGORITHM
    time_quantum: Optional[int] = None
    action: Optional[str] = None
    speed: int = 1

    # ---- Process management ----------------------------------------------

    def add_process(self, process: Process) -> None:
        self.process_list.append(process)

    def remove_process(self, process_id: int) -> None:
        self.process_list = [p for p in self.process_list if p.id != process_id]

    def get_process(self, process_id: int) -> Optional[Process]:
        return next((p for p in self.process_list if p.id == process_id), None)

    def replace_process(self, process_id: int, updated: Process) -> None:
        for index, existing in enumerate(self.process_list):
            if existing.id == process_id:
                self.process_list[index] = updated
                return
        raise ValueError(f"Process {process_id} not found in session {self.session_id}")

    def next_process_id(self) -> int:
        existing_ids = [p.id for p in self.process_list]
        return max(existing_ids, default=0) + 1

    # ---- Scheduler configuration -------------------------------------------

    def set_scheduler(self, algorithm: str, time_quantum: Optional[int] = None) -> None:
        if algorithm not in ALLOWED_ALGORITHMS:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        if algorithm == "ROUND_ROBIN" and not time_quantum:
            raise ValueError("time_quantum is required for ROUND_ROBIN")
        self.algorithm = algorithm
        self.time_quantum = time_quantum if algorithm == "ROUND_ROBIN" else None

    # ---- Simulation control -------------------------------------------------

    def set_action(self, action: str) -> None:
        self.action = action

    def set_speed(self, speed: int) -> None:
        if speed not in ALLOWED_SPEEDS:
            raise ValueError(f"speed must be one of {ALLOWED_SPEEDS}")
        self.speed = speed