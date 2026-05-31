from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.auth import get_current_user
from app.db.connection import get_session
from app.db.models import Budget, Category, User
from app.schemas.budget import BudgetCreate, BudgetRead, BudgetReadWithRelations

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.get("/", response_model=List[BudgetRead])
def budgets_list(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    statement = select(Budget).where(Budget.user_id == current_user.id)
    return session.exec(statement).all()


@router.get("/{budget_id}", response_model=BudgetReadWithRelations)
def budget_get(
    budget_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    budget = session.get(Budget, budget_id)
    if not budget or budget.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


@router.post("/", response_model=BudgetRead)
def budget_create(
    budget_data: BudgetCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    category = session.get(Category, budget_data.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    budget = Budget(
        **budget_data.model_dump(),
        user_id=current_user.id
    )
    session.add(budget)
    session.commit()
    session.refresh(budget)
    return budget


@router.patch("/{budget_id}", response_model=BudgetRead)
def budget_update(
    budget_id: int,
    budget_data: BudgetCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    budget = session.get(Budget, budget_id)
    if not budget or budget.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Budget not found")

    for key, value in budget_data.model_dump(exclude_unset=True).items():
        setattr(budget, key, value)

    budget.user_id = current_user.id

    session.add(budget)
    session.commit()
    session.refresh(budget)
    return budget


@router.delete("/{budget_id}")
def budget_delete(
    budget_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    budget = session.get(Budget, budget_id)
    if not budget or budget.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Budget not found")

    session.delete(budget)
    session.commit()
    return {"ok": True}

@router.get("/{budget_id}/status")
def budget_status(
    budget_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    budget = session.get(Budget, budget_id)
    if not budget or budget.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Budget not found")

    remaining_amount = budget.limit_amount - budget.spent_amount

    return {
        "budget_id": budget.id,
        "title": budget.title,
        "limit_amount": budget.limit_amount,
        "spent_amount": budget.spent_amount,
        "remaining_amount": remaining_amount,
        "is_exceeded": budget.spent_amount > budget.limit_amount,
    }