from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class NoteVisibility(str, Enum):
    private = "private"
    public = "public"
    shared = "shared"


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    visibility: NoteVisibility = NoteVisibility.private
    shared_with_emails: Optional[List[EmailStr]] = None


class NoteUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    visibility: Optional[NoteVisibility]
    shared_with_emails: Optional[list[EmailStr]]

    class Config:
        extra = "forbid"

class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    owner_id: str
    owner_email: Optional[str] = None
    visibility: NoteVisibility
    created_at: datetime
