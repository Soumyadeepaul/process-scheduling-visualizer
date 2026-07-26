from app.strategies.metrics.base_metric import MetricStrategy


class WaitingTime(MetricStrategy):

    def calculate(self, result, scheduleSegments, processList):

        completionTime = {}

        # Find completion time of each process
        for segment in scheduleSegments:
            completionTime[segment.getProcess().getId()] = segment.getEnd()

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