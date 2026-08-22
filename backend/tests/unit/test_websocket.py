"""Unit tests for WebSocket connection and event delivery."""

import asyncio

from app.models.process import Process
from app.models.schedule_segment import ScheduleSegment
from app.websocket.connection_manager import ConnectionManager
from app.websocket.websocket_service import WebSocketService


class FakeWebSocket:
    def __init__(self, fail_on_send=False):
        self.accepted = False
        self.messages = []
        self.fail_on_send = fail_on_send

    async def accept(self):
        self.accepted = True

    async def send_json(self, message):
        if self.fail_on_send:
            raise RuntimeError("connection closed")
        self.messages.append(message)


def run(coroutine):
    return asyncio.run(coroutine)


def test_connection_manager_connects_and_disconnects_a_websocket():
    manager = ConnectionManager()
    websocket = FakeWebSocket()

    run(manager.connect("session-1", websocket))

    assert websocket.accepted is True
    assert manager.getConnection("session-1") is websocket

    manager.disconnect("session-1")
    assert manager.getConnection("session-1") is None


def test_websocket_service_sends_a_process_start_event():
    service = WebSocketService()
    websocket = FakeWebSocket()
    segment = ScheduleSegment(Process(7, 0, 2), 3, 5)
    run(service.connect("session-1", websocket))

    run(service.sendSegment("session-1", segment))

    assert websocket.messages == [{
        "type": "PROCESS_START",
        "data": {"process_id": 7, "start": 3, "end": 5, "state": None},
    }]


def test_websocket_service_sends_completion_and_reset_events():
    service = WebSocketService()
    websocket = FakeWebSocket()
    run(service.connect("session-1", websocket))

    run(service.simulationComplete("session-1"))
    run(service.sendReset("session-1"))

    assert websocket.messages == [
        {"type": "SIMULATION_COMPLETE"},
        {"type": "RESET_COMPLETE"},
    ]


def test_websocket_service_removes_a_connection_that_fails_while_sending():
    service = WebSocketService()
    websocket = FakeWebSocket(fail_on_send=True)
    run(service.connect("session-1", websocket))

    run(service.simulationComplete("session-1"))

    assert service.getConnection("session-1") is None


def test_websocket_service_ignores_events_for_an_unknown_session():
    service = WebSocketService()

    run(service.simulationComplete("missing"))
    run(service.sendSegment("missing", ScheduleSegment(Process(1, 0, 1), 0, 1)))
