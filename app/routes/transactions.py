from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_bank
from app.bank import Banking_system
from app.schemas.bank_schemas import DepositRequest, WithdrawRequest, TransferRequest, MessageResponse, BalanceResposnse
from app.utils import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transcations"])

@router.post("/deposit", response_model = BalanceResposnse)
def deposit_money(data: DepositRequest, bank: Banking_system = Depends(get_bank),  user: str = Depends(get_current_user)):
    new_balance = bank.deposit(data.account_number, data.amount, data.user_id)
    
    return {"message": "Deposit successful", "balance": new_balance}


@router.post("/withdraw", response_model = BalanceResposnse)
def withdraw_money(data: WithdrawRequest, bank: Banking_system = Depends(get_bank),  user: str = Depends(get_current_user)):
    try:
        new_balance = bank.withdraw(data.account_number, data.amount, data.user_id)
        return {"message": "Withdraw successfull", "balance": new_balance}
    except ValueError as e:
        raise HTTPException(status_code=400, detail = str(e))
    
@router.post("/transfer", response_model = MessageResponse)
def transfer_money(data: TransferRequest, bank: Banking_system=Depends(get_bank), user: str = Depends(get_current_user)):
    try:
        bank.transfer(
            data.from_account, 
            data.to_account, 
            data.amount,
            data.user_id)
        return {"message": "Transfer successful"}
    except ValueError as e:
        raise HTTPException(status_code= 400, detail= str(e))

@router.post("/{account_number}")
def transactions_history(account_number: int, bank: Banking_system=Depends(get_bank), user: str = Depends(get_current_user)):
    txns = bank.get_transactions(account_number)

    if not txns:
        raise HTTPException(status_code=404, detail="No transactions found")
    return {"transactions": txns}

