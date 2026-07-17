# Registers all API routers.
from fastapi import APIRouter, Request, HTTPException, WebSocket, WebSocketDisconnect
from app.services.session.session_service import Session
from app.models.session_data import SessionData
from app.factory.process_factory import ProcessFactory
from app.models.process import Process
from app.schemas.process_schema import CreateProcessesRequest, AddProcessRequest
from app.schemas.scheduler_schema import SchedulerRequest
from app.schemas.session_schema import SessionRequest
from app.services.simulation.simulation_service import Simulation
from app.websocket.websocket_instance import websocketService
from app.state.simulation_state_instance import simulationState

router = APIRouter(
    prefix="/api/v1",
    tags=["CPU Scheduler"]
)
        
    
    



# -----------------------
# Data
# -----------------------
__sessionService = Session()
__sessionMap = dict()
__processFactory = ProcessFactory()
__simulationService = Simulation()

# -----------------------
# Session APIs
# -----------------------

@router.post("/session")
def create_session():
    id = __sessionService.createSession()
    __sessionMap[id]=SessionData()
    return { "success": True, "data": { "session_id": id } }


@router.delete("/session/{session_id}")
def delete_session(session_id: str):
    del __sessionMap[id]
    __sessionService.endSession(session_id)
    return { "success": True, "message": "Session deleted" }


# -----------------------
# Process APIs
# -----------------------

@router.post("/processes")
def create_processes(request: CreateProcessesRequest):

    session_id = request.session_id

    if session_id not in __sessionMap:
        raise HTTPException(status_code=404, detail="Session not found")

    processList = __processFactory.createProcess(request.data)

    __sessionMap[session_id].setProcessList(processList)
    
    for process in __sessionMap[session_id].getProcessList():
        print(process.getId())

    return {"success": True}


@router.post("/addprocess", status_code=201)
def add_process(request: AddProcessRequest):

    session_id = request.session_id

    if session_id not in __sessionMap:
        raise HTTPException(status_code=404, detail="Session not found")

    process = Process(
        request.id,
        request.arrival_time,
        request.burst_time,
        request.priority
    )

    __sessionMap[session_id].addProcess(process)
    
    for process in __sessionMap[session_id].getProcessList():
        print(process.getId())

    return {
        "success": True
    }


# @router.put("/processes/{process_id}")
# def update_process(process_id: int):
#     pass


# @router.delete("/processes/{process_id}")
# def delete_process(process_id: int):
#     pass


# # -----------------------
# # Scheduler APIs
# # -----------------------

@router.put("/scheduler")
def update_scheduler(request: SchedulerRequest):

    session_id = request.session_id

    if session_id not in __sessionMap:
        raise HTTPException(status_code=404, detail="Session not found")

    session = __sessionMap[session_id]

    session.setAlgorithm(request.data.algorithm)

    if request.data.algorithm == "ROUND_ROBIN":
        session.setTimeQuantum(request.data.time_quantum)
    else:
        session.setTimeQuantum(None)

    return {
        "success": True
    }
    
    



# # -----------------------
# # Metrics API
# # -----------------------


@router.get("/metrics")
def get_metrics(session_id: str):

    if session_id not in __sessionMap:
        raise HTTPException(
            status_code=404,
            detail="Session not found."
        )

    metrics = simulationState.getMetrics(session_id)

    if metrics is None:
        raise HTTPException(
            status_code=404,
            detail="Metrics not available."
        )

    return {
        "success": True,
        "data": metrics.toDict()
    }

# # -----------------------
# # Websocket API
# # -----------------------



@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):

    await websocketService.connect(session_id, websocket)

    try:

        while True:

            message = await websocket.receive_json()

            action = message["action"]
            session = __sessionMap[session_id]
            session.setAction(action)
            if action == "SPEED":
                session.setSpeed(message["speed"])
            await __simulationService.handleAction(session_id,session)

    except WebSocketDisconnect:
        websocketService.disconnect(session_id)