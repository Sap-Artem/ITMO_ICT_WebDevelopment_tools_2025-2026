from app.db.models import TransactionType
from sqlmodel import SQLModel


class CategoryCreate(SQLModel):
    name: str
    description: str
    transaction_type: TransactionType


class CategoryRead(SQLModel):
    id: int
    name: str
    description: str
    transaction_type: TransactionType