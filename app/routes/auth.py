from fastapi import APIRouter, Depends, HTTPException
from app.schemas.users_schemas import UserCreate, UserResponse, TokenRepsone, RefreshRequest
from app.dependencies import get_users
from app.services.users import Users
from app.utils import create_access_token, create_refresh_token, hash_token
from datetime import datetime, timedelta, timezone 


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user:UserCreate, users: Users = Depends(get_users)):
    new_user = users.register_user(user.email, user.password)
    # return {"message": "Registered successfully", 'User': new_user}
    return new_user
    
@router.post("/login", response_model=TokenRepsone)
def login_user(user:UserCreate, users: Users = Depends(get_users)):
    verified_user, refresh_token =  users.login_user(user.email, user.password)
    access_token  = create_access_token(data= {"sub":str(verified_user["id"])})
    return {"access_token":access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=TokenRepsone)
def refresh_acces_token(refresh: RefreshRequest, users: Users =Depends(get_users)):
    incoming_hash = hash_token(refresh.refresh_token)

    token_data= users.db.get_refresh_token_by_hash(incoming_hash)

    if not token_data or token_data['expires_at'] < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expired or invalid")
    
    #Rotation logic:
    users.db.delete_refresh_token(incoming_hash)

    #Generate new pair(refresh and access)
    user_id = token_data['user_d']
    new_access_token  = create_access_token(data= {"sub":str(user_id)})
    new_refresh_raw = create_refresh_token()

    # save new refresh_token
    new_hash = hash_token(new_refresh_raw)
    new_expiry = datetime.now(timezone.utc) + timedelta(days=7)
    users.db.create_refresh_token(user_id, new_hash, new_expiry)
    users.db.commit()

    return {
        "access_token": new_access_token, 
        "refresh_token": new_refresh_raw, 
        "token_type": "bearer"
    }


