# def test_create_accounts(client):
#     response = client.post(
#         '/accounts/create_account',
#         json = {'name': 'new_user', 'user_id': '1c9086c2-ed70-4c34-9e04-42335921a45f' }
#     )
#     data = response.json()
#     assert response.status_code == 201
#     assert "account_number" in data
#     assert data["message"] == "You have successfully created a account"

