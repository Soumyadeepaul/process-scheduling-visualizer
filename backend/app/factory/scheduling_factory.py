from app.strategies.scheduling.fcfs import FCFS
from app.strategies.scheduling.priority_non_preemptive import PRIORITY
from app.strategies.scheduling.priority_preemptive import PRIORITY_pre
from app.strategies.scheduling.sjf_non_preemptive import SJF
from app.strategies.scheduling.sjf_preemptive import SRTF
from app.strategies.scheduling.round_robin import RR


class SchedulingFactory:

    def getStrategy(self, algorithm):

        if algorithm == "FCFS":
            return FCFS()

        if algorithm == "ROUND_ROBIN":
            return RR()

        if algorithm == "SJF":
            return SJF()
        
        if algorithm == "SRTF":
            return SRTF()
        
        if algorithm == "PRIORITY":
            return PRIORITY()
        
        if algorithm == "PRIORITY_PREEMPTIVE":
            return PRIORITY_pre()

        return None