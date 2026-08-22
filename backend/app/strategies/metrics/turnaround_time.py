from app.strategies.metrics.base_metric import MetricStrategy


class TurnAroundTime(MetricStrategy):

    def calculate(self, result, scheduleSegments, processList):

        completionTime = {}

        for segment in scheduleSegments:
            process = segment.getProcess()

            if process is None:
                continue

            completionTime[process.getId()] = segment.getEnd()

        turnaround = {}

        for process in processList:

            pid = process.getId()

            turnaround[pid] = (
                completionTime[pid]
                - process.getArrivalTime()
            )

        breakdown = result.getTurnaroundTime()
        breakdown.setPerProcess(turnaround)
        breakdown.recomputeAverage()