from datetime import datetime
from typing import Optional
from bson import ObjectId


class TaskModel:
    """
    Internal MongoDB representation of a Task
    """

    def __init__(
        self,
        title: str,
        description: Optional[str],
        owner_id: ObjectId,
        status: str = "pending",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        updated_by: Optional[ObjectId] = None,
        _id: Optional[ObjectId] = None,
    ):
        self.id = _id
        self.title = title
        self.description = description
        self.status = status
        self.owner_id = owner_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at
        self.updated_by = updated_by

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "owner_id": self.owner_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "updated_by": self.updated_by,
        }
