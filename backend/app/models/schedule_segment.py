from app.models.process import Process


class ScheduleSegment:

    def __init__(self, process: Process, start: int, end: int):
        self.__process = process
        self.__start = start
        self.__end = end

    # -----------------------
    # Getters
    # -----------------------

    def getProcess(self):
        return self.__process

    def getStart(self):
        return self.__start

    def getEnd(self):
        return self.__end

    # -----------------------
    # Setters
    # -----------------------

    def setProcess(self, process):
        self.__process = process

    def setStart(self, start):
        self.__start = start

    def setEnd(self, end):
        self.__end = end

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
        }