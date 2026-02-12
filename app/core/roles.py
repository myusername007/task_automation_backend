from fastapi import Depends, HTTPException, status
from app.deps import get_current_user

def require_admin(current_user = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin only access"
        )
    return current_user