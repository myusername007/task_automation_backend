from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.deps import get_db
from app.core.roles import require_admin
from app.schemas.task import TaskRead
from app.schemas.task_run import TaskRunRead
from app.services.task_service import TaskService

router = APIRouter(prefix="/admin", tags=["admin"])

task_service = TaskService()

@router.get("/tasks", response_model=list[TaskRead])
def get_all_tasks(
    db: Session = Depends(get_db), 
    current_user = Depends(require_admin),
    limit: int = Query(20, ge=1, le=100),  # default=20, мін=1, макс=100
    offset: int = Query(0, ge=0),  # default=0, мін=0
    status: str | None = None,
    order: str = "desc",
):
    return task_service.list_all(db, limit=limit, offset=offset, status=status, order=order)

@router.get("/tasks/{task_id}/runs", response_model=list[TaskRunRead])
def get_runs_for_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return task_service.list_runs_for_task(db, task_id)

    