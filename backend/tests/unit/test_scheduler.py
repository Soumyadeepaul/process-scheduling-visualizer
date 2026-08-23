"""Unit tests for every CPU scheduling strategy."""

from app.factory.scheduling_factory import SchedulingFactory
from app.models.process import Process
from app.models.process_status import ProcessStatus
from app.models.schedule_segment import ScheduleSegment
from app.strategies.scheduling.fcfs import FCFS
from app.strategies.scheduling.priority_non_preemptive import PRIORITY
from app.strategies.scheduling.priority_preemptive import PRIORITY_pre
from app.strategies.scheduling.round_robin import RR
from app.strategies.scheduling.sjf_non_preemptive import SJF
from app.strategies.scheduling.sjf_preemptive import SRTF


def segment_data(schedule):
    return [
        (segment.getProcess().getId() if segment.getProcess() else None,
         segment.getStart(), segment.getEnd())
        for segment in schedule
    ]


def test_fcfs_runs_processes_in_arrival_order_and_completes_them():
    first = Process(1, 0, 3)
    second = Process(2, 1, 2)

    schedule = FCFS().execute([second, first], None)

    assert segment_data(schedule) == [(1, 0, 3), (2, 3, 5)]
    assert first.getCompletionTime() == 3
    assert second.getCompletionTime() == 5
    assert first.getStatus() == ProcessStatus.COMPLETED
    assert [segment.getState() for segment in schedule] == [
        ProcessStatus.COMPLETED,
        ProcessStatus.COMPLETED,
    ]


def test_round_robin_rotates_ready_processes_using_the_time_quantum():
    first = Process(1, 0, 4)
    second = Process(2, 1, 2)

    schedule = RR().execute([first, second], 2)

    assert segment_data(schedule) == [(1, 0, 2), (2, 2, 4), (1, 4, 6)]
    assert first.getCompletionTime() == 6
    assert second.getCompletionTime() == 4


def test_sjf_selects_the_shortest_available_job_after_current_job_finishes():
    first = Process(1, 0, 5)
    second = Process(2, 1, 2)
    third = Process(3, 1, 1)

    schedule = SJF().execute([first, second, third], None)

    assert segment_data(schedule) == [(1, 0, 5), (3, 5, 6), (2, 6, 8)]


def test_srtf_preempts_a_running_process_for_a_shorter_job():
    first = Process(1, 0, 5)
    second = Process(2, 1, 2)

    schedule = SRTF().execute([first, second], None)

    assert segment_data(schedule) == [(1, 0, 1), (2, 1, 3), (1, 3, 7)]
    assert first.getCompletionTime() == 7
    assert second.getCompletionTime() == 3


def test_non_preemptive_priority_does_not_interrupt_the_running_process():
    first = Process(1, 0, 4, priority=2)
    second = Process(2, 1, 1, priority=1)

    schedule = PRIORITY().execute([first, second], None)

    assert segment_data(schedule) == [(1, 0, 4), (2, 4, 5)]


def test_preemptive_priority_interrupts_for_a_higher_priority_process():
    first = Process(1, 0, 4, priority=2)
    second = Process(2, 1, 1, priority=1)

    schedule = PRIORITY_pre().execute([first, second], None)

    assert segment_data(schedule) == [(1, 0, 1), (2, 1, 2), (1, 2, 5)]


def test_sjf_adds_an_idle_segment_before_the_first_arrival():
    process = Process(1, 3, 2)

    schedule = SJF().execute([process], None)

    assert segment_data(schedule) == [(None, 0, 3), (1, 3, 5)]


def test_scheduling_factory_returns_requested_strategy_and_none_for_unknown_name():
    factory = SchedulingFactory()

    assert isinstance(factory.getStrategy("FCFS"), FCFS)
    assert isinstance(factory.getStrategy("ROUND_ROBIN"), RR)
    assert isinstance(factory.getStrategy("SJF"), SJF)
    assert isinstance(factory.getStrategy("SRTF"), SRTF)
    assert isinstance(factory.getStrategy("PRIORITY"), PRIORITY)
    assert isinstance(factory.getStrategy("PRIORITY_PREEMPTIVE"), PRIORITY_pre)
    assert factory.getStrategy("UNKNOWN") is None


def test_schedule_segment_exposes_and_serializes_its_state():
    segment = ScheduleSegment(Process(1, 0, 2), 0, 2, state="running")

    assert segment.getState() == "running"
    assert segment.toDict()["state"] == "running"

    segment.setState("completed")
    assert segment.getState() == "completed"
