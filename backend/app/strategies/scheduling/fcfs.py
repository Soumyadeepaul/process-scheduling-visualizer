# FCFS scheduling algorithm.

from app.strategies.scheduling.base_strategy import SchedulingStrategy
from app.models.schedule_segment import ScheduleSegment
class FCFS(SchedulingStrategy):
    
    def execute(self, processList, time_qunatum):
        
        # fcfs algo
        
        #return list of ScheduleSegemnt
        s= ScheduleSegment(100,2,3)
        s1= ScheduleSegment(122,12,12)
        return [s,s1]