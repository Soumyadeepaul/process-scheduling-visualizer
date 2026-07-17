# Stores runtime simulation state.
from app.models.sim_data import SimData
from app.services.metric.metric_service import MetricService

class SimulationState:

    __dataMap = {}
    __metricService = MetricService()

    def setSchedule(self, session_id, scheduleSegments, processList):

        simData = SimData()
        simData.setSchedule(scheduleSegments)
        simData.setProcessList(processList)

        metrics = self.__metricService.calculate(
            scheduleSegments,
            processList
        )

        simData.setMetrics(metrics)
        self.__dataMap[session_id] = simData

    def appendSchedule(self, session_id, scheduleSegments):
        simData = self.__dataMap[session_id]
        simData.getSchedule().extend(scheduleSegments)
        simData.setMetrics(
            self.__metricService.calculate(
                simData.getSchedule(),
                simData.getProcessList()
            )
        )

    def getSchedule(self, session_id):
        print(session_id)
        for key in self.__dataMap.keys():
            print(key)
        return self.__dataMap.get(session_id)

    def getCurrentTime(self, session_id):
        return self.__dataMap[session_id].getCurrentTime()

    def setCurrentTime(self, session_id, time):
        self.__dataMap[session_id].setCurrentTime(time)

    def getMetrics(self, session_id):
        return self.__dataMap[session_id].getMetrics()

    def setMetrics(self, session_id, metrics):
        self.__dataMap[session_id].setMetrics(metrics)

    def removeSchedule(self, session_id):
        self.__dataMap.pop(session_id, None)