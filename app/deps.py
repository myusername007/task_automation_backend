from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_token
from app.services.user_service import UserService 
from app.db.session import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    try: 
        user_id = int(decode_token(token))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = UserService().get_by_id(db,user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

