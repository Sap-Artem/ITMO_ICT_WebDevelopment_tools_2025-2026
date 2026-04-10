from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.auth import get_current_user
from app.db.connection import get_session
from app.db.models import Tag, User
from app.schemas.tag import TagCreate, TagRead

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=List[TagRead])
def tags_list(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return session.exec(select(Tag)).all()


@router.get("/{tag_id}", response_model=TagRead)
def tag_get(
    tag_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.post("/", response_model=TagRead)
def tag_create(
    tag_data: TagCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    tag = Tag.model_validate(tag_data)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


@router.patch("/{tag_id}", response_model=TagRead)
def tag_update(
    tag_id: int,
    tag_data: TagCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    for key, value in tag_data.model_dump(exclude_unset=True).items():
        setattr(tag, key, value)

    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


@router.delete("/{tag_id}")
def tag_delete(
    tag_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    session.delete(tag)
    session.commit()
    return {"ok": True}