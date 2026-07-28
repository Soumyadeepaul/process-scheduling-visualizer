from app.strategies.metrics.base_metric import MetricStrategy


class TurnAroundTime(MetricStrategy):

    def calculate(self, result, scheduleSegments, processList):

        completionTime = {}

        # Find completion time of each process
        for segment in scheduleSegments:
            completionTime[segment.getProcess().getId()] = segment.getEnd()

        turnaround = {}

        for process in processList:

            pid = process.getId()

            turnaround[pid] = (
                completionTime[pid]
                - process.getArrivalTime()
            )

        breakdown = result.getTurnAroundTime()
        breakdown.setPerProcess(turnaround)
        breakdown.recomputeAverage()