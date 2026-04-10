from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.auth import get_current_user
from app.db.connection import get_session
from app.db.models import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserRead])
def users_list(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> List[UserRead]:
    users = session.exec(select(User)).all()
    return [UserRead(id=user.id, username=user.username, email=user.email) for user in users]


@router.get("/{user_id}", response_model=UserRead)
def user_get(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserRead(id=user.id, username=user.username, email=user.email)