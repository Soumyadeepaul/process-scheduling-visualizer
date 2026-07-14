# Process request schemas.
from pydantic import BaseModel
from typing import List, Optional

class ProcessModel(BaseModel):
    id: int
    arrival_time: int
    burst_time: int
    priority: Optional[int]


class CreateProcessesRequest(BaseModel):
    session_id: str
    data: List[ProcessModel]
    



class AddProcessRequest(BaseModel):
    session_id: str
    id: int
    arrival_time: int
    burst_time: int
    priority: Optional[int] = None