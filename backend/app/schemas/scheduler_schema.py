# Scheduler request schemas.
from pydantic import BaseModel
from typing import Optional


class SchedulerData(BaseModel):
    algorithm: str
    time_quantum: Optional[int] = None


class SchedulerRequest(BaseModel):
    session_id: str
    data: SchedulerData