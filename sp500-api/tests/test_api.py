"""
Basic API tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_list_models():
    """Test list models endpoint"""
    response = client.get("/api/v1/models")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

