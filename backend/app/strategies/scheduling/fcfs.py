<<<<<<< HEAD
# FCFS scheduling algorithm.
=======
                                                                                                                                             # FCFS scheduling algorithm.

>>>>>>> 74cc0da3c37809ef4619c6af45b135cf833c1586
from app.strategies.scheduling.base_strategy import SchedulingStrategy
from app.models.schedule_segment import ScheduleSegment
from app.models.process_status import ProcessStatus


class FCFS(SchedulingStrategy):

    def execute(self, processList, timeQuantum, startTime=0):

        schedule = []
        currentTime = startTime

        # Only schedule processes that are not yet completed
        processes = sorted(
            [p for p in processList if p.getRemainingTime() > 0],
            key=lambda p: (p.getArrivalTime(), p.getId())
        )

        for process in processes:

            # If the process arrives after the current time,
            # CPU remains idle until its arrival.
            if currentTime < process.getArrivalTime():
                currentTime = process.getArrivalTime()

            # Skip processes that have already finished
            if process.getRemainingTime() == 0:
                continue

            process.setStatus(ProcessStatus.RUNNING)

            # Preserve the original start time
            if process.getStartTime() is None:
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

            # Process completed
            process.setRemainingTime(0)
            process.setCompletionTime(end)
            process.setStatus(ProcessStatus.COMPLETED)

        return schedule