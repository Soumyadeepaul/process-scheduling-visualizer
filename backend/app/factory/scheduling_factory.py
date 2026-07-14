from app.strategies.scheduling.fcfs import FCFS

class SchedulingFactory:

    def getStrategy(self, algorithm):

        if algorithm == "FCFS":
            return FCFS()

        # if algorithm == "ROUND_ROBIN":
        #     return RoundRobin()

        # if algorithm == "SJF":
        #     return SJF()

        return None