"""
ScheduleSegment domain model.

The atomic output unit of any SchedulingStrategy.execute() call -
equivalent to a single bar in the Gantt chart. A `process` of None
represents CPU idle time between two busy segments.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.models.process import Process


@dataclass
class ScheduleSegment:
    """One contiguous block of CPU time assigned to a process (or idle)."""

    process: Optional[Process]
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.end < self.start:
            raise ValueError("ScheduleSegment.end must be >= start")

    @property
    def duration(self) -> int:
        return self.end - self.start

    @property
    def is_idle(self) -> bool:
        return self.process is None

    def contains_tick(self, tick: int) -> bool:
        return self.start <= tick < self.end

    def to_dict(self) -> dict:
        """Serialize to the exact JSON shape used in the GANTT_CHART
        WebSocket payload."""
        return {
            "process_id": self.process.id if self.process else None,
            "start": self.start,
            "end": self.end,
        }
