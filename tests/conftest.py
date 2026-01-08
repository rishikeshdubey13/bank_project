import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.db
@pytest.fixture
def authorized_client(client):
    response = client.post(
        "/users/login",
        json = {"email": "new_user@test.com", "password": "pass123"}
    )
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})  
    return client