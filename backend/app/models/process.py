from typing import Optional

from app.models.process_status import ProcessStatus


class Process:

    def __init__(
        self,
        processId: int,
        arrivalTime: int,
        burstTime: int,
        priority: Optional[int] = None
    ):
        self.__id = processId
        self.__arrivalTime = arrivalTime
        self.__burstTime = burstTime
        self.__priority = priority

        self.__remainingTime = burstTime
        self.__status = ProcessStatus.WAITING
        self.__startTime = None
        self.__completionTime = None

    # -----------------------
    # Getters
    # -----------------------

    def getId(self):
        return self.__id

    def getArrivalTime(self):
        return self.__arrivalTime

    def getBurstTime(self):
        return self.__burstTime

    def getPriority(self):
        return self.__priority

    def getRemainingTime(self):
        return self.__remainingTime

    def getStatus(self):
        return self.__status

    def getStartTime(self):
        return self.__startTime

    def getCompletionTime(self):
        return self.__completionTime

    def getColor(self):
        return self.__color

    # -----------------------
    # Setters
    # -----------------------

    def setArrivalTime(self, arrivalTime):
        self.__arrivalTime = arrivalTime

    def setBurstTime(self, burstTime):
        self.__burstTime = burstTime

    def setPriority(self, priority):
        self.__priority = priority

    def setRemainingTime(self, remainingTime):
        self.__remainingTime = remainingTime

    def setStatus(self, status):
        self.__status = status

    def setStartTime(self, startTime):
        self.__startTime = startTime

    def setCompletionTime(self, completionTime):
        self.__completionTime = completionTime


    # -----------------------
    # Helper Methods
    # -----------------------

    def hasArrived(self, currentTime):
        return currentTime >= self.__arrivalTime

    def isCompleted(self):
        return self.__status == ProcessStatus.COMPLETED

    def reset(self):
        self.__remainingTime = self.__burstTime
        self.__status = ProcessStatus.WAITING
        self.__startTime = None
        self.__completionTime = None

    def toDict(self):
        return {
            "id": self.__id,
            "arrival_time": self.__arrivalTime,
            "burst_time": self.__burstTime,
            "priority": self.__priority,
            "remaining_time": self.__remainingTime,
            "status": self.__status.value,
            "start_time": self.__startTime,
            "completion_time": self.__completionTime,
        }