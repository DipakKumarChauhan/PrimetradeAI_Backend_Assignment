from fastapi import APIRouter, Depends
from app.utils.dependencies import get_current_user, require_role
from app.schemas.user import UserResponse
from app.core import database
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def read_me(current_user=Depends(get_current_user)):
    return {
        "id": str(current_user["_id"]),
        "email": current_user["email"],
        "role": current_user["role"]
    }


@router.get("", response_model=List[UserResponse])
def get_all_users(admin=Depends(require_role("admin"))):
    """Get all users (Admin only)"""
    users_col = database.get_user_collection()
    users = users_col.find({})
    
    return [
        {
            "id": str(user["_id"]),
            "email": user["email"],
            "role": user["role"],
            "created_at": user.get("created_at")
        }
        for user in users
    ]


@router.get("/admin-only")
def admin_only(admin=Depends(require_role("admin"))):
    return {"message": "Welcome admin"}
