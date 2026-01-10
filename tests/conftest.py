import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def authorized_client(client):
    response = client.post(
        "/users/login",
        json = {"email": "testuser", "password": "testpass"}
    )
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})  
    return client