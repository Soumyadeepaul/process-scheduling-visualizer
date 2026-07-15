from copy import deepcopy


class ScheduleReviser:

    def revise(self, simData, processList):

        # Remove future schedule
        del simData.getSchedule()[simData.getCurrentSegmentIndex():]

        revisedProcessList = []

        for process in processList:

            # Skip completed processes
            if process.getRemainingTime() <= 0:
                continue

            updatedProcess = deepcopy(process)

            # Remaining execution becomes the new burst
            updatedProcess.setBurstTime(
                process.getRemainingTime()
            )

            revisedProcessList.append(updatedProcess)

        return revisedProcessList