from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    balance: float = 1000

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    balance: float
    is_active: bool

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str