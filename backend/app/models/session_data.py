from app.models.process import Process


class SessionData:

    def __init__(self, sessionId: str):
        self.__sessionId = sessionId
        self.__processList = []

        self.__algorithm = "FCFS"
        self.__timeQuantum = None

        self.__action = None
        self.__speed = 1

    # -----------------------
    # Getters
    # -----------------------

    def getSessionId(self):
        return self.__sessionId

    def getProcessList(self):
        return self.__processList

    def getAlgorithm(self):
        return self.__algorithm

    def getTimeQuantum(self):
        return self.__timeQuantum

    def getAction(self):
        return self.__action

    def getSpeed(self):
        return self.__speed

    # -----------------------
    # Setters
    # -----------------------

    def setSessionId(self, sessionId):
        self.__sessionId = sessionId

    def setProcessList(self, processList):
        self.__processList = processList

    def setAlgorithm(self, algorithm):
        self.__algorithm = algorithm

    def setTimeQuantum(self, timeQuantum):
        self.__timeQuantum = timeQuantum

    def setAction(self, action):
        self.__action = action

    def setSpeed(self, speed):
        self.__speed = speed

    # -----------------------
    # Process Methods
    # -----------------------

    def addProcess(self, process: Process):
        self.__processList.append(process)

    def removeProcess(self, processId):
        for process in self.__processList:
            if process.getId() == processId:
                self.__processList.remove(process)
                return

    def getProcess(self, processId):
        for process in self.__processList:
            if process.getId() == processId:
                return process
        return None

    def replaceProcess(self, processId, updatedProcess):
        for index in range(len(self.__processList)):
            if self.__processList[index].getId() == processId:
                self.__processList[index] = updatedProcess
                return

    def getNextProcessId(self):
        if len(self.__processList) == 0:
            return 1

        maxId = 0

        for process in self.__processList:
            if process.getId() > maxId:
                maxId = process.getId()

        return maxId + 1

    # -----------------------
    # Scheduler Methods
    # -----------------------

    def setScheduler(self, algorithm, timeQuantum=None):
        self.__algorithm = algorithm

        if algorithm == "ROUND_ROBIN":
            self.__timeQuantum = timeQuantum
        else:
            self.__timeQuantum = None