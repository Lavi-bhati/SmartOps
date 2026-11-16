
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Application is running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_warning():
    response = client.get("/demo/warning")
    assert response.status_code == 200


def test_logs():
    response = client.get("/logs")
    assert response.status_code == 200
