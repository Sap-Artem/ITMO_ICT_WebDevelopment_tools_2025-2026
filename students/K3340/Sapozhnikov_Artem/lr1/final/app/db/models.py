from enum import Enum
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class TransactionTagLink(SQLModel, table=True):
    transaction_id: Optional[int] = Field(default=None, foreign_key="transaction.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    note: Optional[str] = None
    priority: Optional[int] = None


class UserBase(SQLModel):
    username: str
    email: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str

    transactions: List["Transaction"] = Relationship(back_populates="user")
    budgets: List["Budget"] = Relationship(back_populates="user")
    goals: List["FinancialGoal"] = Relationship(back_populates="user")


class CategoryBase(SQLModel):
    name: str
    description: str
    transaction_type: TransactionType


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    transactions: List["Transaction"] = Relationship(back_populates="category")
    budgets: List["Budget"] = Relationship(back_populates="category")


class TagBase(SQLModel):
    name: str


class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    transactions: List["Transaction"] = Relationship(
        back_populates="tags",
        link_model=TransactionTagLink
    )


class TransactionBase(SQLModel):
    title: str
    amount: float
    transaction_type: TransactionType
    comment: Optional[str] = ""
    user_id: int = Field(foreign_key="user.id")
    category_id: int = Field(foreign_key="category.id")


class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user: Optional[User] = Relationship(back_populates="transactions")
    category: Optional[Category] = Relationship(back_populates="transactions")
    tags: List[Tag] = Relationship(
        back_populates="transactions",
        link_model=TransactionTagLink
    )


class BudgetBase(SQLModel):
    title: str
    limit_amount: float
    spent_amount: float = 0
    user_id: int = Field(foreign_key="user.id")
    category_id: int = Field(foreign_key="category.id")


class Budget(BudgetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user: Optional[User] = Relationship(back_populates="budgets")
    category: Optional[Category] = Relationship(back_populates="budgets")


class FinancialGoalBase(SQLModel):
    title: str
    target_amount: float
    current_amount: float = 0
    deadline: Optional[str] = None
    user_id: int = Field(foreign_key="user.id")


class FinancialGoal(FinancialGoalBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user: Optional[User] = Relationship(back_populates="goals")