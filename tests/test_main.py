
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Application is running"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_warning(client):
    response = client.get("/demo/warning")
    assert response.status_code == 200


def test_logs(client):
    response = client.get("/logs")
    assert response.status_code == 200

