

from app.strategies.scheduling.base_strategy import SchedulingStrategy
from app.models.schedule_segment import ScheduleSegment
from app.models.process_status import ProcessStatus
from collections import deque

# Preemptive SRTF Preemptive algorithm.

class SRTF(SchedulingStrategy):

    def execute(self, processList, timeQuantum, startTime=0):

        schedule = []

        currentTime = startTime

        remaining = processList.copy()

        ready = []  # Initialize the ready list

        while ready or remaining:
            # Filter processes that have arrived
            arrived = [p for p in remaining if p.getArrivalTime() <= currentTime]


            for process in arrived:
                if process.getStatus() == ProcessStatus.WAITING:
                    process.setStatus(ProcessStatus.READY)
                ready.append(process)  # Add the process to the ready list
                remaining.remove(process) #remove the process from remaining
                

            if not ready:
                if not remaining:
                    break

                nextArrival = min(remaining, key=lambda p: p.getArrivalTime())

                schedule.append(
                    ScheduleSegment(
                        None,
                        currentTime,
                        nextArrival.getArrivalTime()
                    )
                )   

                currentTime = nextArrival.getArrivalTime()
                continue
            

            
            
            # SJF: Burst Time -> Arrival Time -> Process ID
            process = min(ready, key=lambda p: (p.getRemainingTime(), p.getArrivalTime(), p.getId()))

            process.setStatus(ProcessStatus.RUNNING)
            if(process.getStartTime() is None):
                process.setStartTime(currentTime)
            
        

            if ( schedule and schedule[-1].getProcess() == process and schedule[-1].getEnd() == currentTime):
                schedule[-1].setEnd(currentTime + 1)
            else:
                schedule.append(
                    ScheduleSegment(
                    process,
                    currentTime,
                    currentTime + 1
        )
    )

            currentTime +=1

            process.setRemainingTime(
                process.getRemainingTime() - 1
            )

            if process.getRemainingTime() == 0:
                process.setCompletionTime(currentTime)
                process.setStatus(ProcessStatus.COMPLETED)
                ready.remove(process)
            else:
                process.setStatus(ProcessStatus.READY)


        return schedule