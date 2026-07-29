from app.strategies.metrics.waiting_time import WaitingTime
from app.strategies.metrics.turnaround_time import TurnAroundTime
from app.strategies.metrics.response_time import ResponseTime
from app.strategies.metrics.completion_time import CompletionTime
from app.strategies.metrics.cpu_utilization import CpuUtilization

class MetricsFactory:

    def getMetrics(self):

        return [
            WaitingTime(),
            TurnAroundTime(),
            ResponseTime(),
            CompletionTime(),
            CpuUtilization()
        ]