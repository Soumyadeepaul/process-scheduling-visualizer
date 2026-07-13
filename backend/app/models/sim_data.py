from typing import List

from app.models.metrics_result import MetricsResult
from app.models.process import Process
from app.models.process_status import ProcessStatus
from app.models.schedule_segment import ScheduleSegment


class SimData:

    def __init__(self, sessionId: str):
        self.__sessionId = sessionId
        self.__schedule = []
        self.__currentTime = 0
        self.__metrics = None
        self.__processList = []

    # -----------------------
    # Getters
    # -----------------------

    def getSessionId(self):
        return self.__sessionId

    def getSchedule(self):
        return self.__schedule

    def getCurrentTime(self):
        return self.__currentTime

    def getMetrics(self):
        return self.__metrics

    def getProcessList(self):
        return self.__processList

    # -----------------------
    # Setters
    # -----------------------

    def setSessionId(self, sessionId):
        self.__sessionId = sessionId

    def setSchedule(self, schedule: List[ScheduleSegment]):
        self.__schedule = schedule

    def setCurrentTime(self, currentTime):
        self.__currentTime = currentTime

    def setMetrics(self, metrics: MetricsResult):
        self.__metrics = metrics

    def setProcessList(self, processList: List[Process]):
        self.__processList = processList

    # -----------------------
    # Schedule Methods
    # -----------------------

    def appendSchedule(self, segments: List[ScheduleSegment]):
        self.__schedule.extend(segments)

    def getSegmentsUpTo(self, tick):
        return [segment for segment in self.__schedule if segment.getStart() <= tick]

    def getSegmentAt(self, tick):
        for segment in self.__schedule:
            if segment.containsTick(tick):
                return segment
        return None

    # -----------------------
    # Clock Methods
    # -----------------------

    def advance(self, ticks=1):
        self.__currentTime += ticks

    def rewind(self, ticks=1):
        self.__currentTime = max(0, self.__currentTime - ticks)

    def reset(self):
        self.__schedule.clear()
        self.__currentTime = 0
        self.__metrics = None

        for process in self.__processList:
            process.reset()

    # -----------------------
    # Runtime Views
    # -----------------------

    def getReadyQueue(self):
        ready = []

        for process in self.__processList:
            if process.getStatus() == ProcessStatus.READY:
                ready.append(process.getId())

        return ready

    def getRunningProcessId(self):
        for process in self.__processList:
            if process.getStatus() == ProcessStatus.RUNNING:
                return process.getId()

        return None

    def getCompletedQueue(self):
        completed = []

        for process in self.__processList:
            if process.getStatus() == ProcessStatus.COMPLETED:
                completed.append(process)

        completed.sort(key=lambda p: p.getCompletionTime() or 0)

        return [process.getId() for process in completed]