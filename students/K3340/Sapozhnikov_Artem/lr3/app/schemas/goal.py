from typing import Optional

from sqlmodel import SQLModel

from app.schemas.user import UserRead


class FinancialGoalCreate(SQLModel):
    title: str
    target_amount: float
    current_amount: float = 0
    deadline: Optional[str] = None


class FinancialGoalRead(SQLModel):
    id: int
    title: str
    target_amount: float
    current_amount: float
    deadline: Optional[str] = None
    user_id: int


class FinancialGoalReadWithRelations(FinancialGoalRead):
    user: UserRead