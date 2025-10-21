from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.config import settings
from app.models import User
from app.schemas.user import UserResponse, UserCreate
from app.schemas.auth import Token
from app.dependencies import get_db, get_current_active_user
from app.auth_utils import verify_password, get_password_hash, create_access_token


router = APIRouter(prefix="", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=404,
            detail="User already created!"
        )

    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=404,
            detail="Wrong email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=404,
            detail="Inactive User",
        )

    access_token_expires = timedelta(minutes=settings.access_expires_minutes)
    access_token = create_access_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify-token")
def verify_token(current_user: User = Depends(get_current_active_user)):
    return {
        "valid": True,
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "balance": current_user.balance,
            "is_active": current_user.is_active
        }
    }
