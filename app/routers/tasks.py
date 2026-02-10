from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.schemas.task_run import TaskRunRead
from app.services.task_service import TaskService
from app.services.task_runner import TaskRunner

from app.db.session import SessionLocal

router = APIRouter(prefix="/tasks", tags=["tasks"])
service = TaskService()
run_service = TaskRunner()

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
    task = service.get_mine_by_id(db, current_user.id, task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return task

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

@router.post("/{task_id}/start", status_code=status.HTTP_200_OK)
def task_run(
    task_id: int,
    background_tasks: BackgroundTasks,  # ← параметр від FastAPI
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # 1. Перевірка task
    task = service.get_mine_by_id(db, current_user.id, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    
    # 2. Перевірка активних запусків
    if run_service.is_active_run(db, task_id):
        raise HTTPException(400, "Task is already running")
    
    # 3. Створюємо TaskRun (status="pending")
    taskrun = run_service.create_run(db, task_id)
    if not taskrun:
        raise HTTPException(status_code=400, detail="Task is already running")
    
    # 4. ‼️ НЕ ЗМІНЮЙ Task.status тут - це зробить background job!
    
    # 5. Запускаємо background job
    background_tasks.add_task( 
        run_service.run_task,
        SessionLocal,
        task.id,
        taskrun.id
    )
    
    # 6. Повертаємо
    return {"run_id": taskrun.id, "status": "pending"}

@router.get("/{task_id}/runs", response_model=list[TaskRunRead], status_code=status.HTTP_200_OK)
def list_runs(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task = service.get_mine_by_id(db, current_user.id, task_id)
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    
    return task.runs
    
       

    
