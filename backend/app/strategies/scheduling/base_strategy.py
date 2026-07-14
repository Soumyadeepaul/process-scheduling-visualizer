# Base scheduling strategy interface.
from abc import ABC, abstractmethod

class SchedulingStrategy(ABC):
    
    @abstractmethod
    def execute(self, session_id, processList, time_qunatum):
        pass