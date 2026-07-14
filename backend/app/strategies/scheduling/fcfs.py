# FCFS scheduling algorithm.

from app.strategies.scheduling.base_strategy import SchedulingStrategy
from app.models.schedule_segment import ScheduleSegment
class FCFS(SchedulingStrategy):
    
    def execute(self, processList, time_qunatum):
        
        # fcfs algo
        
        #return list of ScheduleSegemnt
        s= ScheduleSegment(processList[0],0,3)
        s1= ScheduleSegment(processList[1],3,9)
        s2= ScheduleSegment(processList[0],15,19)
        s3= ScheduleSegment(processList[1],19,20)
        s4= ScheduleSegment(processList[1],25,26)
        s5= ScheduleSegment(processList[1],35,45)
        s6= ScheduleSegment(processList[1],45,50)
        
        
        return [s,s1,s2,s3,s4,s5,s6]