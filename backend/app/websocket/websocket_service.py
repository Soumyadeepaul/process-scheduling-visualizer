from fastapi import WebSocketDisconnect

from app.websocket.connection_manager import ConnectionManager


class WebSocketService:

    def __init__(self):
        self.__manager = ConnectionManager()

    async def connect(self, session_id, websocket):
        print("WebSocketService instance:", id(self))
        await self.__manager.connect(session_id, websocket)

    def disconnect(self, session_id):
        self.__manager.disconnect(session_id)

    def getConnection(self, session_id):
        return self.__manager.getConnection(session_id)

    async def sendSegment(self, session_id, segment):

        websocket = self.__manager.getConnection(session_id)

        if websocket is None:
            print(f"No active websocket for session {session_id}")
            return

        try:
            await websocket.send_json(
                {
                    "type": "PROCESS_START",
                    "data": segment.toDict()
                }
            )
        except (WebSocketDisconnect, RuntimeError):
            self.disconnect(session_id)

    async def simulationComplete(self, session_id):

        websocket = self.__manager.getConnection(session_id)

        if websocket is None:
            return

        try:
            await websocket.send_json(
                {
                    "type": "SIMULATION_COMPLETE"
                }
            )
        except (WebSocketDisconnect, RuntimeError):
            self.disconnect(session_id)
    
    async def sendReset(self, session_id):

        websocket = self.__manager.getConnection(session_id)

        if websocket is None:
            return

        await websocket.send_json(
            {
                "type": "RESET_COMPLETE"
            }
        )