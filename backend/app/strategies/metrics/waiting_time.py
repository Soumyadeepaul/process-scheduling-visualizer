from app.strategies.metrics.base_metric import MetricStrategy


class WaitingTime(MetricStrategy):

    def calculate(self, result, scheduleSegments, processList):

        completionTime = {}

        for segment in scheduleSegments:
            process = segment.getProcess()

            if process is None:
                continue

            completionTime[process.getId()] = segment.getEnd()

        waiting = {}

        for process in processList:

            pid = process.getId()

            waiting[pid] = (
                completionTime[pid]
                - process.getArrivalTime()
                - process.getBurstTime()
            )

        breakdown = result.getWaitingTime()
        breakdown.setPerProcess(waiting)
        breakdown.recomputeAverage()