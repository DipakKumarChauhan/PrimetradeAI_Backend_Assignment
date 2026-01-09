from datetime import datetime
from typing import Optional
from bson import ObjectId


class UserModel:
    """
    Internal MongoDB representation of a User.
    Not exposed directly via API responses.
    """

    def __init__(
        self,
        email: str,
        password_hash: str,
        role: str = "user",
        created_at: Optional[datetime] = None,
        _id: Optional[ObjectId] = None,
    ):
        self.id = _id
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role,
            "created_at": self.created_at,
        }
