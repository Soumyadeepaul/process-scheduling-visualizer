# Manages WebSocket connections.

from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.__connections = {}

    async def connect(self, sessionId, websocket: WebSocket):
        await websocket.accept()
        self.__connections[sessionId] = websocket

    def disconnect(self, sessionId):
        if sessionId in self.__connections:
            del self.__connections[sessionId]

    def getConnection(self, sessionId):
        return self.__connections.get(sessionId)