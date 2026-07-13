"""
Process domain model.

The fundamental unit of simulation. One instance exists per process
created by the user (POST /api/v1/processes). Instances are created
exclusively through ProcessFactory.create_processes() so that id
assignment, defaults, and validation stay centralized in one place.

Field reference (mirrors the JSON shape used by the API/WebSocket
contracts):

    id               int              auto-assigned, read-only
    arrival_time     int              tick the process enters the ready queue
    burst_time       int              total CPU time required
    priority         int | None       used only by priority-based strategies
    remaining_time   int              read-only, updated live by the scheduler
    status           ProcessStatus    read-only
    start_time       int | None       tick of first CPU allocation
    completion_time  int | None       tick of completion
    color            str              hex color for consistent UI rendering
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from app.models.process_status import ProcessStatus

DEFAULT_COLOR = "#4F46E5"


@dataclass
class Process:
    """A single process participating in the CPU scheduling simulation."""

    id: int
    arrival_time: int
    burst_time: int
    priority: Optional[int] = None
    remaining_time: int = field(default=0)
    status: ProcessStatus = field(default=ProcessStatus.WAITING)
    start_time: Optional[int] = None
    completion_time: Optional[int] = None
    color: str = DEFAULT_COLOR

    def __post_init__(self) -> None:
        if self.arrival_time < 0:
            raise ValueError("arrival_time must be >= 0")
        if self.burst_time <= 0:
            raise ValueError("burst_time must be > 0")
        if self.priority is not None and self.priority < 0:
            raise ValueError("priority must be >= 0")
        if self.remaining_time == 0:
            self.remaining_time = self.burst_time

    # ---- Getters --------------------------------------------------------

    def get_id(self) -> int:
        return self.id

    def get_arrival_time(self) -> int:
        return self.arrival_time

    def get_burst_time(self) -> int:
        return self.burst_time

    def get_priority(self) -> Optional[int]:
        return self.priority

    def get_remaining_time(self) -> int:
        return self.remaining_time

    def get_status(self) -> ProcessStatus:
        return self.status

    def get_start_time(self) -> Optional[int]:
        return self.start_time

    def get_completion_time(self) -> Optional[int]:
        return self.completion_time

    def get_color(self) -> str:
        return self.color

    # ---- Setters --------------------------------------------------------

    def set_arrival_time(self, arrival_time: int) -> None:
        self.arrival_time = arrival_time

    def set_burst_time(self, burst_time: int) -> None:
        self.burst_time = burst_time

    def set_priority(self, priority: Optional[int]) -> None:
        self.priority = priority

    def set_remaining_time(self, remaining_time: int) -> None:
        self.remaining_time = max(0, remaining_time)
        if self.remaining_time == 0:
            self.status = ProcessStatus.COMPLETED

    def set_status(self, status: ProcessStatus) -> None:
        self.status = status

    def set_start_time(self, start_time: int) -> None:
        # First allocation only; response time depends on this staying fixed.
        if self.start_time is None:
            self.start_time = start_time

    def set_completion_time(self, completion_time: int) -> None:
        self.completion_time = completion_time

    def set_color(self, color: str) -> None:
        self.color = color

    # ---- Convenience ------------------------------------------------------

    def is_completed(self) -> bool:
        return self.status == ProcessStatus.COMPLETED

    def has_arrived(self, current_time: int) -> bool:
        return current_time >= self.arrival_time

    def reset_runtime_state(self) -> None:
        """Used by ScheduleReviser / SchedulerService.reset() to return the
        process to its pre-simulation state while preserving user input."""
        self.remaining_time = self.burst_time
        self.status = ProcessStatus.WAITING
        self.start_time = None
        self.completion_time = None

    def to_dict(self) -> dict:
        """Serialize to the exact JSON shape expected by the frontend."""
        return {
            "id": self.id,
            "arrival_time": self.arrival_time,
            "burst_time": self.burst_time,
            "priority": self.priority,
            "remaining_time": self.remaining_time,
            "status": self.status.value,
            "start_time": self.start_time,
            "completion_time": self.completion_time,
            "color": self.color,
        }
