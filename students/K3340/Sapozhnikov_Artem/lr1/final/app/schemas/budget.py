from sqlmodel import SQLModel

from app.schemas.category import CategoryRead
from app.schemas.user import UserRead


class BudgetCreate(SQLModel):
    title: str
    limit_amount: float
    spent_amount: float = 0
    category_id: int


class BudgetRead(SQLModel):
    id: int
    title: str
    limit_amount: float
    spent_amount: float
    user_id: int
    category_id: int


class BudgetReadWithRelations(BudgetRead):
    user: UserRead
    category: CategoryRead