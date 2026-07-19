from app.strategies.metrics.waiting_time import WaitingTime
class MetricsFactory:

    def getMetrics(self):

        return [
            WaitingTime(),
            # TurnaroundTime(),
            # ResponseTime(),
            # CompletionTime(),
            # CpuUtilization()
        ]