# Registers all API routers.
from fastapi import APIRouter, Request, HTTPException
from app.services.session.session_service import Session
from app.models.session_data import SessionData
from app.factory.process_factory import ProcessFactory
from app.models.process import Process
from app.schemas.process_schema import CreateProcessesRequest, AddProcessRequest
from app.schemas.scheduler_schema import SchedulerRequest
from app.schemas.session_schema import SessionRequest
from app.services.simulation.simulation_service import Simulation

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

    sessionId = request.session_id

    if sessionId not in __sessionMap:
        raise HTTPException(status_code=404, detail="Session not found")

    processList = __processFactory.createProcess(request.data)

    __sessionMap[sessionId].setProcessList(processList)
    
    for process in __sessionMap[sessionId].getProcessList():
        print(process.getId())

    return {"success": True}


@router.post("/addprocess", status_code=201)
def add_process(request: AddProcessRequest):

    sessionId = request.session_id

    if sessionId not in __sessionMap:
        raise HTTPException(status_code=404, detail="Session not found")

    process = Process(
        request.id,
        request.arrival_time,
        request.burst_time,
        request.priority
    )

    __sessionMap[sessionId].addProcess(process)
    
    for process in __sessionMap[sessionId].getProcessList():
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

    sessionId = request.session_id

    if sessionId not in __sessionMap:
        raise HTTPException(status_code=404, detail="Session not found")

    session = __sessionMap[sessionId]

    session.setAlgorithm(request.data.algorithm)

    if request.data.algorithm == "ROUND_ROBIN":
        session.setTimeQuantum(request.data.time_quantum)
    else:
        session.setTimeQuantum(None)

    return {
        "success": True
    }

# # -----------------------
# # Simulation APIs
# # -----------------------

@router.post("/simulation/play")
def play_simulation(request : SessionRequest):
    
    session_id = request.session_id

    if session_id not in __sessionMap:
        raise HTTPException(status_code=404, detail="Session not found")

    session = __sessionMap[session_id]

    # Update current action
    session.setAction("PLAY")
    
    __simulationService.handleAction(session_id,session)
    
    


@router.post("/simulation/pause")
def pause_simulation(request : SessionRequest):
    session_id = request.session_id

    if session_id not in __sessionMap:
        raise HTTPException(status_code=404, detail="Session not found")

    session = __sessionMap[session_id]

    # Update current action
    session.setAction("PAUSE")
    
    __simulationService(session_id,session)


@router.post("/simulation/resume")
def resume_simulation(request : SessionRequest):
    session_id = request.session_id

    if session_id not in __sessionMap:
        raise HTTPException(status_code=404, detail="Session not found")

    session = __sessionMap[session_id]

    # Update current action
    session.setAction("RESUME")
    
    __simulationService(session_id,session)


# @router.post("/simulation/reset")
# def reset_simulation():
#     pass


# @router.post("/simulation/step")
# def step_simulation():
#     pass


# @router.post("/simulation/previous")
# def previous_step():
#     pass


# @router.post("/simulation/forward")
# def forward_step():
#     pass


# @router.put("/simulation/speed")
# def change_speed():
#     pass


# # -----------------------
# # Metrics API
# # -----------------------

# @router.get("/metrics")
# def get_metrics():
#     pass