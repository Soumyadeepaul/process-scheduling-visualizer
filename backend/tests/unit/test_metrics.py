"""Unit tests for scheduling metric strategies."""

from app.models.metrics_result import MetricsResult
from app.models.process import Process
from app.models.schedule_segment import ScheduleSegment
from app.strategies.metrics.completion_time import CompletionTime
from app.strategies.metrics.cpu_utilization import CpuUtilization
from app.strategies.metrics.response_time import ResponseTime
from app.strategies.metrics.turnaround_time import TurnAroundTime
from app.strategies.metrics.waiting_time import WaitingTime


def make_schedule():
    """Return a schedule where process 1 is preempted and resumes later."""
    process_1 = Process(1, arrivalTime=0, burstTime=5)
    process_2 = Process(2, arrivalTime=1, burstTime=2)
    segments = [
        ScheduleSegment(process_1, 0, 2),
        ScheduleSegment(process_2, 2, 4),
        ScheduleSegment(process_1, 4, 7),
    ]
    return [process_1, process_2], segments


def test_completion_time_stores_a_per_process_mapping():
    processes, segments = make_schedule()
    result = MetricsResult()

    CompletionTime().calculate(result, segments, processes)

    assert result.getCompletionTime() == {1: 7, 2: 4}
    assert result.toDict()["completion_time"] == {"1": 7, "2": 4}


def test_completion_time_uses_the_last_segment_for_a_preempted_process():
    processes, segments = make_schedule()
    result = MetricsResult()

    CompletionTime().calculate(result, segments, processes)

    assert result.getCompletionTime()[1] == 7


def test_waiting_time_calculates_per_process_values_and_average():
    processes, segments = make_schedule()
    result = MetricsResult()

    WaitingTime().calculate(result, segments, processes)

    breakdown = result.getWaitingTime()
    assert breakdown.getPerProcess() == {1: 2, 2: 1}
    assert breakdown.getAverage() == 1.5


def test_turnaround_time_calculates_per_process_values_and_average():
    processes, segments = make_schedule()
    result = MetricsResult()

    TurnAroundTime().calculate(result, segments, processes)

    breakdown = result.getTurnaroundTime()
    assert breakdown.getPerProcess() == {1: 7, 2: 3}
    assert breakdown.getAverage() == 5.0


def test_response_time_calculates_per_process_values_and_average():
    processes, segments = make_schedule()
    result = MetricsResult()

    ResponseTime().calculate(result, segments, processes)

    breakdown = result.getResponseTime()
    assert breakdown.getPerProcess() == {1: 0, 2: 1}
    assert breakdown.getAverage() == 0.5


def test_cpu_utilization_calculates_busy_time_percentage():
    processes, segments = make_schedule()
    result = MetricsResult()

    CpuUtilization().calculate(result, segments, processes)

    assert result.getCpuUtilization() == 100.0
