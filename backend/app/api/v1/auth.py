from fastapi import APIRouter, HTTPException, status
from pymongo.errors import DuplicateKeyError

from app.core import database
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.models.user import UserModel

router = APIRouter(prefix="/auth", tags=["Auth"])
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate):
    users = database.get_user_collection()

    user = UserModel(
        email=payload.email,
        password_hash=hash_password(payload.password),
        role="user"
    )

    try:
        result = users.insert_one(user.to_dict())
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    return {
        "id": str(result.inserted_id),
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at
    }
@router.post("/login")
def login_user(payload: UserLogin):
    users = database.get_user_collection()

    user = users.find_one({"email": payload.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token({
        "sub": str(user["_id"]),
        "role": user["role"]
    })

    return {"access_token": token, "token_type": "bearer"}
