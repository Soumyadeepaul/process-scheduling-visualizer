"""Integration tests for the available FastAPI application surface."""

from fastapi.testclient import TestClient

from app.main import app


def test_home_endpoint_returns_the_application_identity():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "CPU Scheduler Simulator API"}


def test_openapi_schema_exposes_the_cpu_scheduler_metadata():
    client = TestClient(app)

    response = client.get("/openapi.json")
    schema = response.json()

    assert response.status_code == 200
    assert schema["info"]["title"] == "CPU Scheduler Simulator API"
    assert schema["info"]["version"] == "1.0.0"
