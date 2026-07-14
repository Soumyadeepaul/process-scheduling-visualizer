# Executes scheduling workflow.
from app.factory.scheduling_factory import SchedulingFactory
from app.state.simulation_state import SimilationState
class SchedulerService:
    
    __schedulingFactory = SchedulingFactory()
    __similationState = SimilationState()
    
    def computeInitial(self, session_id, processList, algorithm , time_qunatum):
        print(session_id)
        for i in processList:
            print(i.getId(),end="")
        print(algorithm)
        print(time_qunatum)
        strategy = self.__schedulingFactory.getStrategy(algorithm)
        self.__similationState.setSchedule(session_id, strategy.execute(processList,time_qunatum))  #will get  list of Schedule Segment
        # self.__similationState.getSchedule(session_id)
        