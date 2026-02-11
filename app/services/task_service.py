from sqlalchemy.orm import Session
from app.db.models.task import Task
from app.schemas.task import TaskUpdate
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
    
    def list_mine(self, db: Session, owner_id: int, limit=20, offset=0) -> list[Task]:
        return self._base_query(db).filter(Task.owner_id == owner_id).offset(offset).limit(limit).all()
    
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
        
    def _base_query(self, db: Session):
        return db.query(Task).filter(Task.is_deleted == False)
        
    


