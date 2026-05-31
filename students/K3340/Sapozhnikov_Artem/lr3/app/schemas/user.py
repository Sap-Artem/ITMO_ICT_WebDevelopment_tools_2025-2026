from typing import Optional

from sqlmodel import SQLModel


class UserCreate(SQLModel):
    username: str
    email: str
    password: str


class UserLogin(SQLModel):
    username: str
    password: str


class UserRead(SQLModel):
    id: int
    username: str
    email: str


class ChangePassword(SQLModel):
    old_password: str
    new_password: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(SQLModel):
    user_id: Optional[int] = None