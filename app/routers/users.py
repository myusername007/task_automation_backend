from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService
from app.core.roles import require_admin

router = APIRouter(prefix="/users", tags=["users"])
service = UserService()


@router.get("", response_model=list[UserRead])
def list_users(db:Session = Depends(get_db)):
    return service.list(db)

@router.get("/me", response_model=UserRead)
def me(current_user = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    to_find = service.get_by_id(db, user_id)
    if not to_find:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return to_find


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    to_delete = service.get_by_id(db, user_id)
    if not to_delete:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    service.soft_delete(db, to_delete)
