from app.services.scheduler.scheduler_service import SchedulerService
from app.websocket.websocket_instance import websocketService
from app.state.simulation_state_instance import simulationState

import asyncio


class Simulation:

    __schedulerService = SchedulerService()

    __tasks = {}
    __paused = {}
    __speed = {}

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

            self.__speed[session_id] = session_data.getSpeed()

            self.__tasks[session_id] = asyncio.create_task(
                self.__runSimulation(session_id)
            )

        elif action == "PAUSE":

            self.__paused[session_id] = True

        elif action == "RESUME":

            self.__paused[session_id] = False
        elif action == "RESET":

            task = self.__tasks.get(session_id)

            if task and not task.done():
                task.cancel()
            self.__tasks.pop(session_id, None)
            self.__paused.pop(session_id, None)
            simData = simulationState.getSchedule(session_id)

            if simData:
                simData.reset()
            await websocketService.sendReset(session_id)
            
        elif action == "SPEED":
            
            self.__speed[session_id] = session_data.getSpeed()
    async def __runSimulation(self, session_id):

        try:

            simData = simulationState.getSchedule(session_id)

            if simData is None:
                return

            previous_end = 0

            for segment in simData.getSchedule():

                # Current simulation speed
                speed = self.__speed.get(session_id, 1)

                # Initial idle time
                idle = segment.getStart() - previous_end

                if idle > 0:
                    await asyncio.sleep(idle / speed)

                await websocketService.sendSegment(
                    session_id,
                    segment
                )

                # Process executes completely
                await asyncio.sleep(segment.getDuration() / speed)

                # Update simulation clock
                simData.setCurrentTime(segment.getEnd())

                previous_end = segment.getEnd()

                # Pause after current process finishes
                while self.__paused.get(session_id, False):
                    await asyncio.sleep(0.1)

            # Simulation completed normally
            await websocketService.simulationComplete(session_id)

        except asyncio.CancelledError:

            print(f"Simulation {session_id} reset.")

            # Don't send SIMULATION_COMPLETE on reset
            raise

        finally:

            # Cleanup runtime state
            self.__tasks.pop(session_id, None)
            self.__paused.pop(session_id, None)