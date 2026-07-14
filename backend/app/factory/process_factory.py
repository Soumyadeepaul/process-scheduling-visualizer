# Creates process objects from input.

from app.models.process import Process


class ProcessFactory:

    def createProcess(self, data):

        processList = []

        for process in data:
            p = Process(
                process.id,
                process.arrival_time,
                process.burst_time,
                process.priority
            )
            processList.append(p)

        return processList