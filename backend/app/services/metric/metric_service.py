from app.factory.metric_factory import MetricsFactory
from app.models.metrics_result import MetricsResult


class MetricService:

    def __init__(self):
        self.__metrics = MetricsFactory().getMetrics()

    def calculate(self, scheduleSegments, processList):

        result = MetricsResult()

        for metric in self.__metrics:
            metric.calculate(result, scheduleSegments, processList)

        return result