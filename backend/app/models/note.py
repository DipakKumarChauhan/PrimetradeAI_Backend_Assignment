from datetime import datetime
from typing import Optional, List
from bson import ObjectId


class NoteModel:
    """
    Internal MongoDB representation of a Note
    """

    def __init__(
        self,
        title: str,
        content: str,
        owner_id: ObjectId,
        visibility: str = "private",
        shared_with: Optional[List[ObjectId]] = None,
        created_at: Optional[datetime] = None,
        _id: Optional[ObjectId] = None,
    ):
        self.id = _id
        self.title = title
        self.content = content
        self.owner_id = owner_id
        self.visibility = visibility
        self.shared_with = shared_with or []
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "owner_id": self.owner_id,
            "visibility": self.visibility,
            "shared_with": self.shared_with,
            "created_at": self.created_at,
        }
