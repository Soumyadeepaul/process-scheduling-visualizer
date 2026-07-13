"""
Process status enumeration.

Represents the lifecycle state of a Process as it moves through the
scheduling simulation:

    WAITING   -> process has not yet arrived (current_time < arrival_time)
    READY     -> arrived, sitting in the ready queue
    RUNNING   -> currently allocated to the CPU
    COMPLETED -> finished execution (remaining_time == 0)
"""

from enum import Enum


class ProcessStatus(str, Enum):
    """Lifecycle states for a simulated process."""

    WAITING = "waiting"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.value