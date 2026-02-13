from sqlalchemy.orm import Session
from app.db.models.task import Task
from app.schemas.task import TaskUpdate, TaskCreate, TaskRead
from app.db.models.task_run import TaskRun
from typing import Optional

class TaskService:
    def create(self, db: Session, owner_id: int, title: str, description: Optional[str]) -> Task:
        task = Task(
            owner_id = owner_id,
            title = title,
            description = description
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    
    def list_mine(
            self, 
            db: Session, 
            owner_id: int, 
            limit: int = 20, 
            offset: int = 0,
            status: str | None = None,
            order: str = "desc",
        ) -> list[Task]:
        
        query = self._base_query(db).filter(Task.owner_id == owner_id)
        if status:
            query = query.filter(Task.status == status)
        if order == "asc":
            query = query.order_by(Task.created_at.asc())
        else: 
            query = query.order_by(Task.created_at.desc())
        return query.limit(limit).offset(offset).all()
    
    def get_mine_by_id(self, db: Session, owner_id: int, task_id: int) -> Task | None:
        return self._base_query(db).filter(Task.owner_id == owner_id, Task.id == task_id).first()
    
    def update_mine(self, db: Session, task: Task, payload: TaskUpdate) -> Task:
        update_data = payload.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)
        return task
    
    def soft_delete_mine(self, db: Session, task: Task) -> None:
        task.is_deleted = True
        db.commit()

    def list_all(
            self, 
            db: Session, 
            limit: int = 50, 
            offset: int = 0,
            status: str | None = None,
            order: str = "desc",
        ) -> list[Task]:
        query = self._base_query(db)
        if status:
            query = query.filter(Task.status == status)
        if order == "asc":
            query = query.order_by(Task.created_at.asc())
        else: 
            query = query.order_by(Task.created_at.desc())
        return query.limit(limit).offset(offset).all()
    
    def list_runs_for_task(self, db: Session, task_id: int) -> list[TaskRun]:
        return db.query(TaskRun).filter(TaskRun.task_id == task_id).all()
        
    def _base_query(self, db: Session):
        return db.query(Task).filter(Task.is_deleted == False)
        
    


