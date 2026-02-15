from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TaskRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    task_id: int
    status: str
    message: Optional[str] = None
    started_at: datetime
    finished_at: Optional[datetime] = None

    