from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.deps import get_db
from app.schemas.user import UserCreate, UserRead
from app.schemas.token import Token
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.core.security import get_password_hash, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])
users = UserService()
auth = AuthService()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if users.get_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed = get_password_hash(payload.password)
    user = users.create(db, payload.email, hashed)
    return user

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_id = auth.login(db, form.username, form.password)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user_id)
    return {"access_token": token, "token_type": "bearer"}