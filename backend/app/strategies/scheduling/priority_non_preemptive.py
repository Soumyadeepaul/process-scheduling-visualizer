

from app.strategies.scheduling.base_strategy import SchedulingStrategy
from app.models.schedule_segment import ScheduleSegment
from app.models.process_status import ProcessStatus


# Non-preemptive Priority algorith.

class PRIORITY(SchedulingStrategy):

    def execute(self, processList, timeQuantum, startTime=0):
        
        schedule = []

        currentTime = startTime

        remaining = processList.copy()

        while remaining:

            #Filter Process That Have Arrived
            arrived = [p for p in remaining if p.getArrivalTime() <=currentTime]

            if not arrived:
                #No process have Arrived
                nextArrival = min(remaining, key=lambda p:p.getArrivalTime())

                schedule.append(
                    ScheduleSegment(
                        None,
                        currentTime,
                        nextArrival.getArrivalTime()
                    )
                )
                currentTime=nextArrival.getArrivalTime()
                continue

            ready = []  # Initialize the ready list

            for process in arrived:
                if process.getStatus() == ProcessStatus.WAITING:
                    process.setStatus(ProcessStatus.READY)
                ready.append(process)  # Add the process to the ready list

            #lew priority number high priority 1>2>3>4.....
            process = min(ready, key=lambda p: (p.getPriority(), p.getArrivalTime(), p.getId()))

            process.setStatus(ProcessStatus.RUNNING)
            if(process.getStartTime() is None):
                process.setStartTime(currentTime)
            
            start = currentTime
            end = start + process.getRemainingTime()
            schedule.append(
                ScheduleSegment(
                    process,
                    start,
                    end
                )
            )

            currentTime = end

            process.setRemainingTime(0)
            process.setCompletionTime(end)
            process.setStatus(ProcessStatus.COMPLETED)

            remaining.remove(process)

        return schedule
