from sqlalchemy.orm import Session
import time
from datetime import datetime
from app.db.models.task_run import TaskRun
from app.db.models.task import Task

class TaskRunner:
    def run_task(self, db_factory, task_id: int, run_id: int) -> None:
        """Background job для виконання задачі"""
        db: Session = db_factory()
        
        try:
            # Отримуємо TaskRun
            task_run = db.query(TaskRun).filter(TaskRun.id == run_id).first()
            if not task_run:
                return
            
            # Отримуємо Task
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                task_run.status = "failed"
                task_run.message = f"Task {task_id} not found"
                task_run.finished_at = datetime.utcnow()
                db.commit()
                return
            
            # ‼️ змінюємо статуси на "running"
            task_run.status = "running"
            task_run.started_at = datetime.utcnow()
            task.status = "running"  # ← Task теж на running
            db.commit()
            
            # Імітація роботи
            time.sleep(30)
            
            # Завершення
            task.result = f"processed: {task.title}"
            task.status = "done"
            task_run.status = "done"
            task_run.finished_at = datetime.utcnow()
            db.commit()
            
        except Exception as e:
            # Обробка помилок
            if task_run:
                task_run.status = "failed"
                task_run.message = str(e)
                task_run.finished_at = datetime.utcnow()
            if task:
                task.status = "failed"
            db.commit()
            
        finally:
            db.close()
    
    def is_active_run(self, db: Session, task_id: int) -> bool:
        """Перевіряє наявність активного запуску"""
        return db.query(TaskRun).filter(
            TaskRun.task_id == task_id,
            TaskRun.status.in_(["pending", "running"])
        ).first() is not None
    
    def create_run(self, db: Session, task_id: int) -> TaskRun:
        active = db.query(TaskRun).filter(
        TaskRun.task_id == task_id,
        TaskRun.status.in_(["pending", "running"])
        ).first()
        if active:
            return None

        """Створює новий TaskRun зі статусом pending"""
        task_run = TaskRun(task_id=task_id)  # ← default="pending"
        db.add(task_run)
        db.commit()
        db.refresh(task_run)
        return task_run