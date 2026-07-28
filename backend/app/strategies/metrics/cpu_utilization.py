from app.strategies.metrics.base_metric import MetricStrategy


class CpuUtilization(MetricStrategy):

    def calculate(self, result, scheduleSegments, processList):

        busyTime = 0

        for segment in scheduleSegments:

            busyTime += (
                segment.getEnd()
                - segment.getStart()
            )

        totalTime = scheduleSegments[-1].getEnd()

        utilization = 0

        if totalTime > 0:
            utilization = (busyTime / totalTime) * 100

        result.setCpuUtilization(utilization)