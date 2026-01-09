from fastapi import APIRouter, Depends
from app.utils.dependencies import get_current_user, require_role

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def read_me(current_user=Depends(get_current_user)):
    return {
        "id": str(current_user["_id"]),
        "email": current_user["email"],
        "role": current_user["role"]
    }


@router.get("/admin-only")
def admin_only(admin=Depends(require_role("admin"))):
    return {"message": "Welcome admin"}
