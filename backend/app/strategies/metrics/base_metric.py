# Base metric strategy interface.
from abc import ABC, abstractmethod


class MetricStrategy(ABC):
    
    @abstractmethod
    def calculate(self,result, scheduleSegment, processList):
        pass