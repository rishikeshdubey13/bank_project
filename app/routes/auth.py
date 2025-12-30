from fastapi import APIRouter, Depends
from app.schemas.users_schemas import UserCreate, UserResponse, TokenRepsone
from app.dependencies import get_users
from app.services.users import Users
from app.utils import create_access_token



router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user:UserCreate, users: Users = Depends(get_users)):
    new_user = users.register_user(user.email, user.password)
    # return {"message": "Registered successfully", 'User': new_user}
    return new_user
    
@router.post("/login", response_model=TokenRepsone)
def login_user(user:UserCreate, users: Users = Depends(get_users)):
    verified_user =  users.login_user(user.email, user.password)
    access_token  = create_access_token(data= {"sub":str(verified_user["id"])})
    return {"access_token":access_token, "token_type": "bearer"}

