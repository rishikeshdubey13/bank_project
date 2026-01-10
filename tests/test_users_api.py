import pytest

@pytest.mark.db
def test_register_user(client):
    response = client.post(
        "/users/register",
        json={"email": "new_user2@test.com", "password": "pass123"}
    )

    assert response.status_code == 201
    assert response.json()["email"] == "new_user2@test.com"

@pytest.mark.db
def test_login_user(client):
    response = client.post(
        "/users/login",
        json = {"email": "new_user2@test.com", "password": "pass123"}
    )
    data = response.json()
    assert response.status_code == 200

    assert "access_token" in data 
    assert data["token_type"] == "bearer" 
    
    # there is not need for email as user already enter the email in the frontent. 
    # Dont need to return it back

@pytest.mark.db
def test_logout_and_token_revocation(client):
    # 1. Login to get a valid refresh token
    login_response = client.post(
        "/users/login",
        json={"email": "new_user2@test.com", "password": "pass123"}
    )
    login_data = login_response.json()
    refresh_token = login_data.get("refresh_token")
    
    # 2. Perform the Logout
    # Note: Adjust the header/body based on how your API expects the token
    logout_response = client.post(
        "/users/logout",
        json={"refresh_token": refresh_token},
        headers={"Authorization": f"Bearer {login_data['access_token']}"}
    )
    assert logout_response.status_code == 200
    # assert logout_response.json()["message"] == "Successfully logged out"

    # 3. VERIFICATION: Try to use the revoked refresh token
    # This is the "negative test" that proves revocation worked
    refresh_response = client.post(
        "/users/refresh",
        json={"refresh_token": refresh_token}
    )
    
    # The status should be 401 Unauthorized or 400 Bad Request
    assert refresh_response.status_code == 401
    assert "revoked" in refresh_response.json()["detail"].lower()