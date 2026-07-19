class ScheduleReviser:

    def revise(self, simData, processList):

        currentTime = simData.getCurrentTime()
        currentIndex = simData.getCurrentSegmentIndex()
        schedule = simData.getSchedule()

        scheduledProcessIds = {
            segment.getProcess().getId()
            for segment in schedule
        }

        deletedSegments = schedule[currentIndex:]

        # Restore remaining time
        for i, segment in enumerate(deletedSegments):

            process = segment.getProcess()

            if i == 0:
                restore = max(
                    0,
                    segment.getEnd() - currentTime
                )
            else:
                restore = (
                    segment.getEnd()
                    - segment.getStart()
                )

            process.setRemainingTime(
                process.getRemainingTime() + restore
            )

        # Remove discarded schedule
        del schedule[currentIndex:]

        revisedProcessList = []

        for process in processList:

            # New process
            if process.getId() not in scheduledProcessIds:
                revisedProcessList.append(process)
                continue

            # Completed process
            if process.getRemainingTime() <= 0:
                continue

            process.setBurstTime(
                process.getRemainingTime()
            )

            revisedProcessList.append(process)

        return revisedProcessList