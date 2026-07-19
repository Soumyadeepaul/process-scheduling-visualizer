

from app.strategies.scheduling.base_strategy import SchedulingStrategy
from app.models.schedule_segment import ScheduleSegment
from app.models.process_status import ProcessStatus

# Non-preemptive SJF algorithm.

class SJF(SchedulingStrategy):

    def execute(self, processList, timeQuantum, startTime=0):

        schedule = []

        currentTime = startTime

        remaining = processList.copy()

        while remaining:
            # Filter processes that have arrived
            arrived = [p for p in remaining if p.getArrivalTime() <= currentTime]

            if not arrived:
                # If no process has arrived, move time forward to the next arrival
                next_arrival = min(remaining, key=lambda p: p.getArrivalTime())

                schedule.append(
                    ScheduleSegment(
                        None,  # No process is running
                        currentTime,
                        next_arrival.getArrivalTime()
                    )
                )
                currentTime = next_arrival.getArrivalTime()
                continue

            ready = []  # Initialize the ready list
            for process in arrived:
                if process.getStatus() == ProcessStatus.WAITING:
                    process.setStatus(ProcessStatus.READY)
                ready.append(process)  # Add the process to the ready list

            # SJF: Burst Time -> Arrival Time -> Process ID
            process = min(ready, key=lambda p: (p.getRemainingTime(), p.getArrivalTime(), p.getId()))

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
