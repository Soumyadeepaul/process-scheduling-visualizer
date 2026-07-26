# Waiting time metric strategy.
from app.strategies.metrics.base_metric import MetricStrategy
from app.models.metrics_result import MetricBreakdown


class WaitingTime(MetricStrategy):

    def calculate(self, result, scheduleSegments, processList):

        waitingTime = MetricBreakdown()

        perProcess = {}

        for process in processList:

            completionTime = 0

            for segment in scheduleSegments:
                if segment.getProcess() == process.getId():
                    completionTime = segment.getEnd()

            waiting = (
                completionTime
                - process.getArrivalTime()
                - process.getBurstTime()
            )

            perProcess[process.getId()] = waiting

        waitingTime.setPerProcess(perProcess)
        waitingTime.recomputeAverage()

        result.setWaitingTime(waitingTime)