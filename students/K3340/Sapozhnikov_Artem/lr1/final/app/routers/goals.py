from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.auth import get_current_user
from app.db.connection import get_session
from app.db.models import FinancialGoal, User
from app.schemas.goal import FinancialGoalCreate, FinancialGoalRead, FinancialGoalReadWithRelations

router = APIRouter(prefix="/goals", tags=["goals"])


@router.get("/", response_model=List[FinancialGoalRead])
def goals_list(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    statement = select(FinancialGoal).where(FinancialGoal.user_id == current_user.id)
    return session.exec(statement).all()


@router.get("/{goal_id}", response_model=FinancialGoalReadWithRelations)
def goal_get(
    goal_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    goal = session.get(FinancialGoal, goal_id)
    if not goal or goal.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@router.post("/", response_model=FinancialGoalRead)
def goal_create(
    goal_data: FinancialGoalCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    goal = FinancialGoal(
        **goal_data.model_dump(),
        user_id=current_user.id
    )
    session.add(goal)
    session.commit()
    session.refresh(goal)
    return goal


@router.patch("/{goal_id}", response_model=FinancialGoalRead)
def goal_update(
    goal_id: int,
    goal_data: FinancialGoalCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    goal = session.get(FinancialGoal, goal_id)
    if not goal or goal.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Goal not found")

    for key, value in goal_data.model_dump(exclude_unset=True).items():
        setattr(goal, key, value)

    goal.user_id = current_user.id

    session.add(goal)
    session.commit()
    session.refresh(goal)
    return goal


@router.delete("/{goal_id}")
def goal_delete(
    goal_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    goal = session.get(FinancialGoal, goal_id)
    if not goal or goal.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Goal not found")

    session.delete(goal)
    session.commit()
    return {"ok": True}