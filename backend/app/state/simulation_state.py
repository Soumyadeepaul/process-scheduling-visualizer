# Stores runtime simulation state.
from app.models.sim_data import SimData
class SimilationState:
    __dataMap =dict()
    
    def setSchedule(self, session_id, scheduleSegments):
        simData = SimData()
        simData.setSchedule(scheduleSegments)
        self.__dataMap[session_id]=simData
    
    def getSchedule(self, session_id):
        for i in self.__dataMap[session_id].getSchedule():
            print(i.getProcess())
        return self.__dataMap[session_id]