from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: Optional[str] = None
    status: str
    result: Optional[str] = None
    owner_id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

   
