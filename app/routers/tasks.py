from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])
service = TaskService()

@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    task = service.create(db,current_user.id, payload.title, payload.description)
    return task

@router.get("", response_model=list[TaskRead])
def list_tasks(
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user),
    limit: int = Query(20, ge=1, le=100),  # default=20, мін=1, макс=100
    offset: int = Query(0, ge=0)  # default=0, мін=0
):
    return service.list_mine(db, current_user.id, limit=limit, offset=offset)

@router.get("/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
def get_task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not service.get_mine_by_id(db, current_user.id, task_id):
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return service.get_mine_by_id(db, current_user.id, task_id)

@router.patch("/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
def task_update(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task_to_update = service.get_mine_by_id(db, current_user.id, task_id)

    if not task_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return service.update_mine(db, task_to_update, payload)