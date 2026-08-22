# Base scheduling strategy interface.
from abc import ABC, abstractmethod

class SchedulingStrategy(ABC):
    
    @abstractmethod
    def execute(self, processList, timeQuantum, startTime=0):
        pass