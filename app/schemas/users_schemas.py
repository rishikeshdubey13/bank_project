from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = 'user'

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: str
    is_active: bool

class TokenRepsone(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str