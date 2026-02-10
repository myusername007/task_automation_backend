from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskRunRead(BaseModel):
    id: int
    task_id: int
    status: str
    message: Optional[str] = None
    started_at: datetime
    finished_at: Optional[datetime] = None

    class Config:
        from_attributes: True