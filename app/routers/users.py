from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])
service = UserService()

@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    if db. query(__import__("app.db.models.user").db.models.user.User).filter_by(email = payload.email).first():
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    
    user = service.create(db, payload.email, payload.password)
    return user

@router.get("", response_model=list[UserRead])
def list_users(db:Session = Depends(get_db)):
    return service.list(db)

