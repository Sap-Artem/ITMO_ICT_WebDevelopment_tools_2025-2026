from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.auth import get_current_user
from app.db.connection import get_session
from app.db.models import Transaction, Category, User
from app.schemas.transaction import TransactionCreate, TransactionRead, TransactionReadWithRelations

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/", response_model=List[TransactionRead])
def transactions_list(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    statement = select(Transaction).where(Transaction.user_id == current_user.id)
    return session.exec(statement).all()


@router.get("/{transaction_id}", response_model=TransactionReadWithRelations)
def transaction_get(
    transaction_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    transaction = session.get(Transaction, transaction_id)
    if not transaction or transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.post("/", response_model=TransactionRead)
def transaction_create(
    transaction_data: TransactionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    category = session.get(Category, transaction_data.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    transaction = Transaction(
        **transaction_data.model_dump(),
        user_id=current_user.id
    )
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


@router.patch("/{transaction_id}", response_model=TransactionRead)
def transaction_update(
    transaction_id: int,
    transaction_data: TransactionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    transaction = session.get(Transaction, transaction_id)
    if not transaction or transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in transaction_data.model_dump(exclude_unset=True).items():
        setattr(transaction, key, value)

    transaction.user_id = current_user.id

    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


@router.delete("/{transaction_id}")
def transaction_delete(
    transaction_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    transaction = session.get(Transaction, transaction_id)
    if not transaction or transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")

    session.delete(transaction)
    session.commit()
    return {"ok": True}