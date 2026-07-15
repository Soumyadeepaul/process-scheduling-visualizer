# Executes scheduling workflow.
from app.factory.scheduling_factory import SchedulingFactory
from app.state.simulation_state import SimilationState
from app.services.scheduler.schedule_reviser import ScheduleReviser
from copy import deepcopy
class SchedulerService:
    
    __schedulingFactory = SchedulingFactory()
    __similationState = SimilationState()
    __scheduleReviser = ScheduleReviser()
    
    def computeInitial(self, session_id, processList, algorithm, time_qunatum):

        # Schedule already exists for this session
        if self.__similationState.getSchedule(session_id):
            return

        strategy = self.__schedulingFactory.getStrategy(algorithm)
        
        workingProcessList = deepcopy(processList)

        schedule = strategy.execute(workingProcessList, time_qunatum, 0)

        self.__similationState.setSchedule(session_id, schedule)
    
    
    
    def recompute(self, session_id, processList, algorithm, time_qunatum):

        simData = self.__similationState.getSchedule(session_id)

        if simData is None:
            self.computeInitial(
                session_id,
                processList,
                algorithm,
                time_qunatum
            )
            return

        revisedProcessList = self.__scheduleReviser.revise(
            simData,
            processList
        )

        strategy = self.__schedulingFactory.getStrategy(algorithm)

        # Compute remaining schedule
        newSchedule = strategy.execute(revisedProcessList, time_qunatum, simData.getCurrentTime())

        # TODO:
        # Shift schedule to start from currentTime

        # Append to existing executed schedule
        simData.getSchedule().extend(newSchedule)