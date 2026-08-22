from app.strategies.metrics.base_metric import MetricStrategy


class CpuUtilization(MetricStrategy):

    def calculate(self, result, scheduleSegments, processList):

        busyTime = 0

        for segment in scheduleSegments:
            process = segment.getProcess()

            if process is None:
                continue

            busyTime += (
                segment.getEnd()
                - segment.getStart()
            )

        if not scheduleSegments:
            result.setCpuUtilization(0)
            return

        totalTime = max(
            segment.getEnd()
            for segment in scheduleSegments
        )

        utilization = 0

        if totalTime > 0:
            utilization = (busyTime / totalTime) * 100

        result.setCpuUtilization(utilization)