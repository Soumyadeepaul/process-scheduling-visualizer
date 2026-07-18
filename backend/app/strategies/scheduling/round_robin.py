

from app.strategies.scheduling.base_strategy import SchedulingStrategy
from app.models.schedule_segment import ScheduleSegment
from app.models.process_status import ProcessStatus
from collections import deque


# Round Robin scheduling algorithm.

class RR(SchedulingStrategy):

    def execute(self, processList, timeQuantum, startTime=0):

        schedule = []

        currentTime = startTime

        remaining = processList.copy()

        ready = deque() #Initialize ready queue

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
            

            
            
            # RR
            process = ready.popleft()

            process.setStatus(ProcessStatus.RUNNING)
            if(process.getStartTime() is None):
                process.setStartTime(currentTime)
            
            executed = min(process.getRemainingTime(), timeQuantum)
            
            start = currentTime
            end = start + executed

            schedule.append(
                ScheduleSegment(
                    process,
                    start,
                    end
                )
            )

            currentTime = end

            process.setRemainingTime(
                process.getRemainingTime() - executed
            )

            arrived = [p for p in remaining if p.getArrivalTime() <= currentTime]

            for p in arrived:
                p.setStatus(ProcessStatus.READY)
                ready.append(p)
                remaining.remove(p)

            if process.getRemainingTime() == 0:
                process.setCompletionTime(currentTime)
                process.setStatus(ProcessStatus.COMPLETED)
            else:
                process.setStatus(ProcessStatus.READY)
                ready.append(process)

        return schedule
