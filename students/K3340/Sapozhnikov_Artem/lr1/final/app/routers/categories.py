from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.auth import get_current_user
from app.db.connection import get_session
from app.db.models import Category, User
from app.schemas.category import CategoryCreate, CategoryRead

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryRead])
def categories_list(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return session.exec(select(Category)).all()


@router.get("/{category_id}", response_model=CategoryRead)
def category_get(
    category_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryRead)
def category_create(
    category_data: CategoryCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    category = Category.model_validate(category_data)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.patch("/{category_id}", response_model=CategoryRead)
def category_update(
    category_id: int,
    category_data: CategoryCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in category_data.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.delete("/{category_id}")
def category_delete(
    category_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"ok": True}