from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.auth import get_current_user
from app.db.connection import get_session
from app.db.models import Transaction, TransactionType, Budget, User

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/summary")
def reports_summary(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    transactions = session.exec(
        select(Transaction).where(Transaction.user_id == current_user.id)
    ).all()

    total_income = sum(
        transaction.amount
        for transaction in transactions
        if transaction.transaction_type == TransactionType.income
    )

    total_expense = sum(
        transaction.amount
        for transaction in transactions
        if transaction.transaction_type == TransactionType.expense
    )

    budgets = session.exec(
        select(Budget).where(Budget.user_id == current_user.id)
    ).all()

    exceeded_budgets = [
        {
            "budget_id": budget.id,
            "title": budget.title,
            "limit_amount": budget.limit_amount,
            "spent_amount": budget.spent_amount,
        }
        for budget in budgets
        if budget.spent_amount > budget.limit_amount
    ]

    return {
        "user_id": current_user.id,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense,
        "transactions_count": len(transactions),
        "budgets_count": len(budgets),
        "exceeded_budgets": exceeded_budgets,
    }