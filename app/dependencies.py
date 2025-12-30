from app.database import Database
from app.bank import Banking_system
from app.services.users import Users
from fastapi import Depends

def get_db():
    db = Database()
    try:
        yield db
        # Optional: only commit here if you want ALL successful routes to auto-commit
        # db.commit() 
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def get_bank(db=Depends(get_db)) -> Banking_system:
    return Banking_system(db=db)

def get_users(db=Depends(get_db)) -> Users:
    return Users(db=db)
