from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class User(BaseModel):
    id: int
    username: str
    email: str


class Category(BaseModel):
    id: int
    name: str
    description: str
    transaction_type: TransactionType


class Tag(BaseModel):
    id: int
    name: str


class Budget(BaseModel):
    id: int
    title: str
    limit_amount: float
    spent_amount: float
    category: Category
    user: User


class Goal(BaseModel):
    id: int
    title: str
    target_amount: float
    current_amount: float
    deadline: Optional[str] = None
    user: User


class Transaction(BaseModel):
    id: int
    title: str
    amount: float
    transaction_type: TransactionType
    comment: Optional[str] = ""
    category: Category
    user: User
    tags: Optional[List[Tag]] = []