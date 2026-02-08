from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.core.security import verify_password

class AuthService:
    def login(self, db: Session, email: str, password: str) -> int | None: 
        user = UserService().get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user.id
    
    