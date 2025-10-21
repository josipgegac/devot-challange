from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from typing import Optional
from app.config import settings
from app.schemas.auth import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_expires_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Could not verify creditials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return TokenData(email=email)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not verify creditials",
            headers={"WWW-Authenticate": "Bearer"}
        )