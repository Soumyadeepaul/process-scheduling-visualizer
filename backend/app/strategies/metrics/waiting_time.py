# Waiting time metric strategy.
from app.strategies.metrics.base_metric import MetricStrategy

class WaitingTime(MetricStrategy):
    
    def calculate(self, result, scheduleSegment, processList):
        pass