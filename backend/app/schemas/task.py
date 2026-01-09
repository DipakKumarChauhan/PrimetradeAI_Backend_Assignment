from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending
    assignee_id: Optional[str] = None   # for admin


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatus]

    class Config:
        extra = "forbid"


class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: str
    owner_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None
