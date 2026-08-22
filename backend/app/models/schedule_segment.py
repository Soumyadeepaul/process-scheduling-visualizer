from app.models.process import Process


class ScheduleSegment:

    def __init__(self, process: Process, start: int, end: int, state=None):
        self.__process = process
        self.__start = start
        self.__end = end
        self.__state = state

    # -----------------------
    # Getters
    # -----------------------

    def getProcess(self):
        return self.__process

    def getStart(self):
        return self.__start

    def getEnd(self):
        return self.__end

    def getState(self):
        return self.__state

    # -----------------------
    # Setters
    # -----------------------

    def setProcess(self, process):
        self.__process = process

    def setStart(self, start):
        self.__start = start

    def setEnd(self, end):
        self.__end = end

    def setState(self, state):
        self.__state = state

    # -----------------------
    # Helper Methods
    # -----------------------

    def getDuration(self):
        return self.__end - self.__start

    def isIdle(self):
        return self.__process is None

    def containsTick(self, tick):
        return self.__start <= tick < self.__end

    def toDict(self):
        return {
            "process_id": self.__process.getId() if self.__process else None,
            "start": self.__start,
            "end": self.__end,
            "state": self.__state.value if hasattr(self.__state, "value") else self.__state,
        }
