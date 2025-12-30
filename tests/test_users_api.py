# def test_register_user(client):
#     response = client.post(
#         "/users/register",
#         json={"email": "new_user1@test.com", "password": "pass123"}
#     )

#     assert response.status_code == 201
#     assert response.json()["email"] == "new_user1@test.com"


def test_login_user(client):
    response = client.post(
        "/users/login",
        json = {"email": "new_user@test.com", "password": "pass123"}
    )
    data = response.json()
    assert response.status_code == 200

    assert "access_token" in data 
    assert data["token_type"] == "bearer" 
    
    # there is not need for email as user already enter the email in the frontent. 
    # Dont need to return it back