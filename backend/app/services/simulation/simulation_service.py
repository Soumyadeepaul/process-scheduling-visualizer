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
                self.__runSimulation(session_id, session_data)
            )

        elif action == "PAUSE":

            self.__paused[session_id] = True

        elif action == "RESUME":

            if session_data.isDirty():

                self.__schedulerService.recompute(
                    session_id,
                    session_data.getProcessList(),
                    session_data.getAlgorithm(),
                    session_data.getTimeQuantum()
                )

                session_data.setDirty(False)

            self.__paused[session_id] = False
        elif action == "RESET":

            task = self.__tasks.get(session_id)

            if task and not task.done():
                task.cancel()
            self.__tasks.pop(session_id, None)
            self.__paused.pop(session_id, None)
            simulationState.removeSchedule(session_id)
            await websocketService.sendReset(session_id)
            
        elif action == "SPEED":
            
            self.__speed[session_id] = session_data.getSpeed()
        
            
            
    async def __runSimulation(self, session_id, session_data):

        try:

            simData = simulationState.getSchedule(session_id)

            if simData is None:
                return

            while simData.getCurrentSegmentIndex() < len(simData.getSchedule()):

                segment = simData.getSchedule()[simData.getCurrentSegmentIndex()]

                # Current simulation speed
                speed = self.__speed.get(session_id, 1)

                # Initial idle time
                if simData.getCurrentSegmentIndex() == 0:
                    previous_end = 0
                else:
                    previous_end = simData.getSchedule()[
                        simData.getCurrentSegmentIndex() - 1
                    ].getEnd()

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
                simData.setCurrentSegmentIndex(simData.getCurrentSegmentIndex() + 1)
                

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