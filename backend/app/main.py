# FastAPI application entry point.
from fastapi import FastAPI

from app.api.router import router

app = FastAPI(
    title="CPU Scheduler Simulator API",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "CPU Scheduler Simulator API"
    }