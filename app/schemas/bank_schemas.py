from pydantic import BaseModel
from decimal import Decimal
from uuid import UUID

class AccountCreateResponse(BaseModel):
    account_number:int
    message: str


class AccountCreateRequest(BaseModel):
    name: str
    user_id: UUID

class BalanceResposnse(BaseModel):
    balance: Decimal
    message: str

class MessageResponse(BaseModel):
    message: str

class DepositRequest(BaseModel):
    account_number: int
    amount: Decimal
    user_id: UUID

class WithdrawRequest(BaseModel):
    account_number: int
    amount: Decimal
    user_id: UUID
    

class TransferRequest(BaseModel):
    from_account: int
    to_account: int
    amount: Decimal
    user_id: UUID





