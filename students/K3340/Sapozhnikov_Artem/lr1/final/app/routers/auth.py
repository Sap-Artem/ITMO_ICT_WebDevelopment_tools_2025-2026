from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.auth import get_current_user
from app.core.security import hash_password, verify_password, create_access_token
from app.db.connection import get_session
from app.db.models import User
from app.schemas.user import UserCreate, UserLogin, UserRead, ChangePassword, Token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
def register(user_data: UserCreate, session: Session = Depends(get_session)) -> UserRead:
    existing_user = session.exec(
        select(User).where(User.username == user_data.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    existing_email = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return UserRead(id=user.id, username=user.username, email=user.email)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
) -> Token:
    user = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token)


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)) -> UserRead:
    return UserRead(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
    )


@router.post("/change-password")
def change_password(
    data: ChangePassword,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if not verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    current_user.password_hash = hash_password(data.new_password)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return {"message": "Password changed successfully"}