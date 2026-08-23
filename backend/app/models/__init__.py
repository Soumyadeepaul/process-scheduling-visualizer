"""
Domain model package.

Plain data objects representing the core simulation entities. These
carry no service-layer logic (scheduling algorithms, metric
calculation, session lifecycle) - that logic lives in app/services,
app/strategies, and app/state, and operates on these models.

Exposes every model class so callers can do:

    from app.models import Process, ProcessStatus, ScheduleSegment, ...
"""

from app.models.metrics_result import MetricBreakdown, MetricsResult
from app.models.process import Process
from app.models.process_status import ProcessStatus
from app.models.schedule_segment import ScheduleSegment
from app.models.session_data import SessionData
from app.models.sim_data import SimData

__all__ = [
    "Process",
    "ProcessStatus",
    "ScheduleSegment",
    "SessionData",
    "SimData",
    "MetricsResult",
    "MetricBreakdown",
]