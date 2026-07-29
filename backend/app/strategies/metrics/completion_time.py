from app.strategies.metrics.base_metric import MetricStrategy


class CompletionTime(MetricStrategy):

    def calculate(self, result, scheduleSegments, processList):

        completion = {}

        # Find completion time of each process
        for segment in scheduleSegments:
            completion[segment.getProcess().getId()] = segment.getEnd()

        # Completion time is stored directly as a process-ID-to-time mapping
        # in MetricsResult, unlike the metrics that use MetricBreakdown.
        result.setCompletionTime(completion)
