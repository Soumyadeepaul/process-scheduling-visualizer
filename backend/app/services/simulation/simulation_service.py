# Coordinates simulation execution.

from app.services.scheduler.scheduler_service import SchedulerService 

class Simulation:
    
    __schedulerService = SchedulerService()
    
    def handleAction(self, session_id, session_data):
        
        action=session_data.getAction()
        if(action == "PLAY"):
            #scheduler service
            self.__schedulerService.computeInitial(session_id, session_data.getProcessList(), session_data.getAlgorithm(), session_data.getTimeQuantum())
            # websocket service
            pass
        elif (action == "PAUSE"):
            
            #Stop the websocket
            pass
        elif (action == "RESUME"):
            #resume the websocket
            pass