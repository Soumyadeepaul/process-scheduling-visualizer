# Stores runtime simulation state.
from app.models.sim_data import SimData


class SimilationState:

    __dataMap = dict()

    def setSchedule(self, session_id, scheduleSegments):
        simData = SimData()
        simData.setSchedule(scheduleSegments)
        self.__dataMap[session_id] = simData

    def getSchedule(self, session_id):
        return self.__dataMap.get(session_id)

    def removeSchedule(self, session_id):
        self.__dataMap.pop(session_id, None)