from fastapi import APIRouter, Depends
from app.models import User
from app.schemas.user import UserResponse
from app.dependencies import get_current_active_user


router = APIRouter(tags=["users"])

@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_active_user)):
    return current_user
