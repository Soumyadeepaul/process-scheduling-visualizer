# Executes scheduling workflow.
from app.factory.scheduling_factory import SchedulingFactory
from app.state.simulation_state_instance import simulationState
from app.services.scheduler.schedule_reviser import ScheduleReviser
from copy import deepcopy
class SchedulerService:
    
    __schedulingFactory = SchedulingFactory()
    __scheduleReviser = ScheduleReviser()
    
    def computeInitial(self, session_id, processList, algorithm, time_qunatum):

        

        strategy = self.__schedulingFactory.getStrategy(algorithm)
        
        workingProcessList = deepcopy(processList)

        schedule = strategy.execute(workingProcessList, time_qunatum, 0)
        

        simulationState.setSchedule(session_id, schedule, processList)
    
    
    
    def recompute(self, session_id, processList, algorithm, time_qunatum):

        simData = simulationState.getSchedule(session_id)

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

        simulationState.extendSchedule(session_id,newSchedule)