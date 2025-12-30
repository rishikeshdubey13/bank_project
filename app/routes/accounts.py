
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_bank
from app.bank import Banking_system
from app.schemas.bank_schemas import AccountCreateResponse, BalanceResposnse, AccountCreateRequest
from app.utils import get_current_user
from uuid import UUID

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/create_account", response_model=AccountCreateResponse, status_code=201)
def create_account(payload:AccountCreateRequest, bank: Banking_system = Depends(get_bank), user_id: UUID = Depends(get_current_user)):
    account_number = bank.create_account(payload.name, user_id)
    return {
        "account_number" : account_number,
        "message": "You have successfully created a account"
    }

@router.get("/{account_number}/balance", response_model=BalanceResposnse)
def get_balance(account_number: int, bank: Banking_system = Depends(get_bank), user: str = Depends(get_current_user)):
    balance = bank.show_balance(account_number, user_id=UUID(user))
    if balance is None:
        raise HTTPException(status_code=404, detail="Account not found or unauthorized")
    return {"message": "Balance retrieved successfully", "balance": balance}
