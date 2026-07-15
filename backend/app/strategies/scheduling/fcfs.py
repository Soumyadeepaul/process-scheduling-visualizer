# FCFS scheduling algorithm.

from app.strategies.scheduling.base_strategy import SchedulingStrategy
from app.models.schedule_segment import ScheduleSegment
from app.models.process_status import ProcessStatus


class FCFS(SchedulingStrategy):

    def execute(self, processList, timeQuantum, startTime=0):

        schedule = []

        currentTime = startTime

        # FCFS: Arrival Time -> Process ID
        processes = sorted(
            processList,
            key=lambda p: (p.getArrivalTime(), p.getId())
        )

        for process in processes:

            # CPU idle until process arrives
            if currentTime < process.getArrivalTime():
                currentTime = process.getArrivalTime()

            process.setStatus(ProcessStatus.RUNNING)

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

            # Process completed
            process.setRemainingTime(0)
            process.setCompletionTime(end)
            process.setStatus(ProcessStatus.COMPLETED)

            if process.getStartTime() is None:
                process.setStartTime(start)

        return schedule