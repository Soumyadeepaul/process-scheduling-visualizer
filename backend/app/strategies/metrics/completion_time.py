from app.strategies.metrics.base_metric import MetricStrategy


class CompletionTime(MetricStrategy):

    def calculate(self, result, scheduleSegments, processList):

        completion = {}

        # Find completion time of each process
        for segment in scheduleSegments:
            completion[segment.getProcess().getId()] = segment.getEnd()

        breakdown = result.getCompletionTime()
        breakdown.setPerProcess(completion)
        breakdown.recomputeAverage()