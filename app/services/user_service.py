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
    
    def get_by_email(self, db: Session, user_email: str) -> User | None:
        return db.query(User).filter(User.email == user_email).first()
    
    def get_by_id(self, db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()