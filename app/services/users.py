import psycopg2
from app.utils import hash_password, verify_password, create_refresh_token, hash_token
from datetime import datetime, timedelta, timezone

class Users:
    def __init__(self, db):
        self.db =db

    #serialize user
    # def serialize_user(self,user):
    #     return {
    #         "id": user['id'],
    #         "email": user['email'],
    #         "role": user['role'],
    #         "is_active": user['is_active']  
    #     }
    def serialize_user(self, user):
        if hasattr(user, 'keys') or isinstance(user, dict):
            return {
                "id": user['id'],
                "email": user['email'],
                "is_active": user['is_active'],
                "role": user['role']
                
            }
        # Handle tuple-like objects
        else:
            return {
                "id": user[0],
                "email": user[1],
                "is_active": user[3],
                "role": user[4]
                
        }

    #Register-users
    def register_user(self, email, password):
        if self.db.check_user(email):
            raise ValueError("Email already registered")
        password_hash = hash_password(password)
        try:
            self.db.create_user(email, password_hash)
            self.db.commit()
            user = self.db.check_user(email)
            return self.serialize_user(user)
        except Exception as e:
            self.db.rollback()
            raise RuntimeError("Failed to register user")



    #get_user
    def get_user(self, email):
        user = self.db.check_user(email)
        if not user:
            return None
        return self.serialize_user(user)


    def login_user(self, email, password):
        try:
            user = self.db.check_user(email)
            if not user or not verify_password(password, user['password_hash']):
                raise ValueError("Invalid email or password")
            
            raw_refresh_token = create_refresh_token()
            token_hash = hash_token(raw_refresh_token)
            expires_at = datetime.now(timezone.utc) + timedelta(days=7)

            self.db.create_refresh_token(user['id'], token_hash, expires_at)
            self.db.commit()

            return self.serialize_user(user), raw_refresh_token
        except psycopg2.Error:
            raise RuntimeError("Database error occurred")

       
    def delete_user(self, email):
        success = self.db.delete_user(email)
        if not success:
            raise ValueError(f"User with {email} does not exist or could not be deleted")
        return True
        
#Edit-users

#delete-users
# so whenever i login i need to generate new refresh and acces token, and save the 
# refresh token in DB when access token expire create new referesh token and access token.
#