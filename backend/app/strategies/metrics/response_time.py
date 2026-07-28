from app.strategies.metrics.base_metric import MetricStrategy


class ResponseTime(MetricStrategy):

    def calculate(self, result, scheduleSegments, processList):

        firstStartTime = {}

        # Find the first execution time of each process
        for segment in scheduleSegments:

            pid = segment.getProcess().getId()

            if pid not in firstStartTime:
                firstStartTime[pid] = segment.getStart()

        response = {}

        for process in processList:

            pid = process.getId()

            response[pid] = (
                firstStartTime[pid]
                - process.getArrivalTime()
            )

        breakdown = result.getResponseTime()
        breakdown.setPerProcess(response)
        breakdown.recomputeAverage()