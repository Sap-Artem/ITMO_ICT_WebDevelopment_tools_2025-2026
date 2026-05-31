from typing import Optional, List

from sqlmodel import SQLModel

from app.db.models import TransactionType
from app.schemas.category import CategoryRead
from app.schemas.tag import TagRead
from app.schemas.user import UserRead


class TransactionCreate(SQLModel):
    title: str
    amount: float
    transaction_type: TransactionType
    comment: Optional[str] = ""
    category_id: int


class TransactionRead(SQLModel):
    id: int
    title: str
    amount: float
    transaction_type: TransactionType
    comment: Optional[str] = ""
    user_id: int
    category_id: int


class TransactionReadWithRelations(TransactionRead):
    user: Optional[UserRead] = None
    category: Optional[CategoryRead] = None
    tags: List[TagRead] = []