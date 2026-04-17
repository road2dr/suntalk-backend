import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

with patch("app.database.Base") as mock_base:
    mock_base.metadata = MagicMock()
    with patch("app.database.engine"):
        from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "SunTalk Backend API"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_success():
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_fail():
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "wrong"},
    )
    assert response.status_code == 401