from app.strategies.metrics.base_metric import MetricStrategy


class CompletionTime(MetricStrategy):

    def calculate(self, result, scheduleSegments, processList):

        completion = {}

        for segment in scheduleSegments:
            process = segment.getProcess()

            if process is None:
                continue

            completion[process.getId()] = segment.getEnd()

        result.setCompletionTime(completion)