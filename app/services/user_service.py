from sqlalchemy.orm import Session
from app.db.models.user import User

class UserService:
    def create(self, db: Session, email: str, hashed_password: str) -> User:
        user = User(
            email = email,
            hashed_password = hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def list(self, db: Session) -> list[User]:
        return db.query(User).all()