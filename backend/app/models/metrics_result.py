class MetricBreakdown:

    def __init__(self):
        self.__perProcess = {}
        self.__average = 0.0

    # -----------------------
    # Getters
    # -----------------------

    def getPerProcess(self):
        return self.__perProcess

    def getAverage(self):
        return self.__average

    # -----------------------
    # Setters
    # -----------------------

    def setPerProcess(self, perProcess):
        self.__perProcess = perProcess

    def setAverage(self, average):
        self.__average = average

    # -----------------------
    # Helper Methods
    # -----------------------

    def recomputeAverage(self):
        values = list(self.__perProcess.values())

        if len(values) == 0:
            self.__average = 0.0
        else:
            self.__average = round(sum(values) / len(values), 2)

    def toDict(self):
        return {
            "per_process": {str(key): value for key, value in self.__perProcess.items()},
            "average": self.__average,
        }


class MetricsResult:

    def __init__(self):
        self.__waitingTime = MetricBreakdown()
        self.__turnaroundTime = MetricBreakdown()
        self.__responseTime = MetricBreakdown()
        self.__completionTime = {}
        self.__cpuUtilization = 0.0

    # -----------------------
    # Getters
    # -----------------------

    def getWaitingTime(self):
        return self.__waitingTime

    def getTurnaroundTime(self):
        return self.__turnaroundTime

    def getResponseTime(self):
        return self.__responseTime

    def getCompletionTime(self):
        return self.__completionTime

    def getCpuUtilization(self):
        return self.__cpuUtilization

    # -----------------------
    # Setters
    # -----------------------

    def setWaitingTime(self, waitingTime):
        self.__waitingTime = waitingTime

    def setTurnaroundTime(self, turnaroundTime):
        self.__turnaroundTime = turnaroundTime

    def setResponseTime(self, responseTime):
        self.__responseTime = responseTime

    def setCompletionTime(self, completionTime):
        self.__completionTime = completionTime

    def setCpuUtilization(self, cpuUtilization):
        self.__cpuUtilization = cpuUtilization

    # -----------------------
    # Helper Methods
    # -----------------------

    def toDict(self):
        return {
            "waiting_time": self.__waitingTime.toDict(),
            "turnaround_time": self.__turnaroundTime.toDict(),
            "response_time": self.__responseTime.toDict(),
            "completion_time": {
                str(key): value
                for key, value in self.__completionTime.items()
            },
            "cpu_utilization": round(self.__cpuUtilization, 2),
        }