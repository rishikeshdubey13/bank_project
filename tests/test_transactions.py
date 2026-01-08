
import pytest

@pytest.mark.db
def test_desposit_money(authorized_client):
    desposit_amount =  200.0
    response = authorized_client.post(
        "/transactions/deposit",
        json = {"account_number": 47038468, "amount": desposit_amount, "user_id": "19387672-1c1f-49cb-8c8d-2b72fef61015"}
    )
    data = response.json()
    assert response.status_code == 200
    assert "balance" in data
    # assert float(data["balance"]) == 100.0
    assert data["message"] == "Deposit successful"
@pytest.mark.db
def test_withdraw_money(authorized_client):
    withdraw_amount = 100
    response = authorized_client.post(
        '/transactions/withdraw',
        json = {"account_number": 47038468, "amount": withdraw_amount, "user_id": "19387672-1c1f-49cb-8c8d-2b72fef61015"}
    )
    data =response.json()
    assert response.status_code == 200
    assert "balance" in data
    assert data["message"] == "Withdraw successfull"

@pytest.mark.db
def test_transfer_money(authorized_client):
    transfer_money = 100
    response = authorized_client.post(
        "/transactions/transfer",
        json =  {"from_account":47038468, "to_account":53927463 ,"amount":transfer_money, "user_id": "19387672-1c1f-49cb-8c8d-2b72fef61015"}
    )
    data = response.json()
    # if response.status_code == 422:
    #     print(response.json())
    assert response.status_code == 200
    assert data["message"] == "Transfer successful"
