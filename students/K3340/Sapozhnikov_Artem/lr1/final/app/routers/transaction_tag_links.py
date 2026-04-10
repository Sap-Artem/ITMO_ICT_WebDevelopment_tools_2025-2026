from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.auth import get_current_user
from app.db.connection import get_session
from app.db.models import TransactionTagLink, Transaction, Tag, User
from app.schemas.transaction_tag_link import TransactionTagLinkCreate, TransactionTagLinkRead

router = APIRouter(prefix="/transaction-tag-links", tags=["transaction-tag-links"])


@router.get("/", response_model=List[TransactionTagLinkRead])
def links_list(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    statement = (
        select(TransactionTagLink)
        .join(Transaction, Transaction.id == TransactionTagLink.transaction_id)
        .where(Transaction.user_id == current_user.id)
    )
    return session.exec(statement).all()


@router.post("/", response_model=TransactionTagLinkRead)
def link_create(
    link_data: TransactionTagLinkCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    transaction = session.get(Transaction, link_data.transaction_id)
    if not transaction or transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")

    tag = session.get(Tag, link_data.tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    existing_link = session.get(
        TransactionTagLink,
        (link_data.transaction_id, link_data.tag_id)
    )
    if existing_link:
        raise HTTPException(status_code=400, detail="Link already exists")

    link = TransactionTagLink(**link_data.model_dump())
    session.add(link)
    session.commit()
    session.refresh(link)
    return link