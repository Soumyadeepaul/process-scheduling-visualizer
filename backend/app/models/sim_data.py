"""
SimData domain model.

Concrete per-session runtime record held inside
SimulationState.data_map (keyed by session_id). Tracks the computed
schedule, the current simulation clock, the last computed metrics,
and the reconciled process list at the current tick. This is the
object WebSocketService reads from to build every outgoing snapshot
message (PROCESS_TABLE, READY_QUEUE, RUNNING_PROCESS, COMPLETED_QUEUE,
CPU_STATE, GANTT_CHART, PERFORMANCE_METRICS).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from app.models.metrics_result import MetricsResult
from app.models.process import Process
from app.models.process_status import ProcessStatus
from app.models.schedule_segment import ScheduleSegment


@dataclass
class SimData:
    """Runtime simulation state for a single session."""

    session_id: str
    schedule: List[ScheduleSegment] = field(default_factory=list)
    current_time: int = 0
    metrics: Optional[MetricsResult] = None
    process_list: List[Process] = field(default_factory=list)

    # ---- Schedule access ----------------------------------------------------

    def set_schedule(self, segments: List[ScheduleSegment]) -> None:
        self.schedule = segments

    def append_schedule(self, segments: List[ScheduleSegment]) -> None:
        self.schedule.extend(segments)

    def segments_up_to(self, tick: int) -> List[ScheduleSegment]:
        """Segments that have started by the given tick - what
        ScheduleReviser walks to reconcile process state."""
        return [s for s in self.schedule if s.start <= tick]

    def segment_at(self, tick: int) -> Optional[ScheduleSegment]:
        return next((s for s in self.schedule if s.contains_tick(tick)), None)

    # ---- Clock -----------------------------------------------------------------

    def advance(self, ticks: int = 1) -> None:
        self.current_time += ticks

    def rewind(self, ticks: int = 1) -> None:
        self.current_time = max(0, self.current_time - ticks)

    def reset(self) -> None:
        self.schedule = []
        self.current_time = 0
        self.metrics = None
        for process in self.process_list:
            process.reset_runtime_state()

    # ---- Derived live views (used to build WebSocket snapshots) -----------------

    def ready_queue(self) -> List[int]:
        return [p.id for p in self.process_list if p.status == ProcessStatus.READY]

    def running_process_id(self) -> Optional[int]:
        running = next((p for p in self.process_list if p.status == ProcessStatus.RUNNING), None)
        return running.id if running else None

    def completed_queue(self) -> List[int]:
        completed = [p for p in self.process_list if p.status == ProcessStatus.COMPLETED]
        completed.sort(key=lambda p: p.completion_time or 0)
        return [p.id for p in completed]

    # ---- Metrics -----------------------------------------------------------------

    def set_metrics(self, metrics: MetricsResult) -> None:
        self.metrics = metrics
