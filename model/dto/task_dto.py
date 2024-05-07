from enum import Enum
from datetime import datetime

from pydantic import BaseModel

# enums
class PriorityType(str, Enum):
    high = 'high'
    mid = 'mid'
    low = 'low'

class StatusType(str, Enum):
    completed = 'completed'
    pending = 'pending'

# Dto
class CreateTask(BaseModel):
    title: str
    due_date: datetime | None = None
    priority: PriorityType
    
class UpdateTask(BaseModel):
    task_id: str
    title: str | None = None
    due_date: datetime | None = None
    priority: PriorityType | None = None

class TaskId(BaseModel):
    task_id: str
   