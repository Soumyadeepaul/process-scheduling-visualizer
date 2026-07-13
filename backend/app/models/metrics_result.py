"""
MetricsResult domain model.

Aggregated output of MetricService.compute_metrics(), combining the
result of every registered MetricStrategy (waiting time, turnaround
time, response time, completion time, CPU utilization). Mirrors the
JSON shape returned by GET /api/v1/metrics and pushed via the
PERFORMANCE_METRICS WebSocket message.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class MetricBreakdown:
    """Per-process values plus the average, for a single metric type.

    Used for waiting_time, turnaround_time, and response_time - the
    three metrics that report both an average and a per-process value.
    """

    per_process: Dict[int, float] = field(default_factory=dict)
    average: float = 0.0

    def recompute_average(self) -> None:
        values = list(self.per_process.values())
        self.average = round(sum(values) / len(values), 2) if values else 0.0

    def to_dict(self) -> dict:
        return {
            "per_process": {str(k): v for k, v in self.per_process.items()},
            "average": round(self.average, 2),
        }


@dataclass
class MetricsResult:
    """Full metrics snapshot for a simulation session at a point in time."""

    waiting_time: MetricBreakdown = field(default_factory=MetricBreakdown)
    turnaround_time: MetricBreakdown = field(default_factory=MetricBreakdown)
    response_time: MetricBreakdown = field(default_factory=MetricBreakdown)
    completion_time: Dict[int, int] = field(default_factory=dict)
    cpu_utilization: float = 0.0

    def to_dict(self) -> dict:
        """Serialize to the exact JSON shape used by GET /metrics and the
        PERFORMANCE_METRICS WebSocket message."""
        return {
            "waiting_time": self.waiting_time.to_dict(),
            "turnaround_time": self.turnaround_time.to_dict(),
            "response_time": self.response_time.to_dict(),
            "completion_time": {str(k): v for k, v in self.completion_time.items()},
            "cpu_utilization": round(self.cpu_utilization, 2),
        }
