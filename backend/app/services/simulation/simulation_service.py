from app.services.scheduler.scheduler_service import SchedulerService
from app.websocket.websocket_instance import websocketService
from app.state.simulation_state import SimilationState
from app.state.simulation_state_instance import simulationState

import asyncio


class Simulation:

    __schedulerService = SchedulerService()

    __tasks = {}
    __paused = {}

    async def handleAction(self, session_id, session_data):

        action = session_data.getAction()

        if action == "PLAY":

            self.__schedulerService.computeInitial(
                session_id,
                session_data.getProcessList(),
                session_data.getAlgorithm(),
                session_data.getTimeQuantum()
            )

            self.__paused[session_id] = False

            self.__tasks[session_id] = asyncio.create_task(
                self.__runSimulation(session_id)
            )

        elif action == "PAUSE":

            self.__paused[session_id] = True

        elif action == "RESUME":

            self.__paused[session_id] = False

    async def __runSimulation(self, session_id):

        simData = simulationState.getSchedule(session_id)

        if simData is None:
            return

        previous_end = 0

        for segment in simData.getSchedule():

            # Initial idle time
            idle = segment.getStart() - previous_end

            if idle > 0:
                await asyncio.sleep(idle)

            await websocketService.sendSegment(
                session_id,
                segment
            )

            # Process executes completely
            await asyncio.sleep(segment.getDuration())

            simData.setCurrentTime(segment.getEnd())

            previous_end = segment.getEnd()

            # Pause only AFTER process completion
            while self.__paused.get(session_id, False):
                await asyncio.sleep(0.1)

        await websocketService.simulationComplete(session_id)