from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime
from app.schemas.expense import *
from app.models import User
from app.dependencies import get_current_active_user, filter_expenses, sort_expenses, aggregate_expenses
from app.models import Expense
from app.dependencies import get_db

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("", response_model=Dict[str, List[ExpenseResponse]])
def get_expenses(
        id: int | None = None,
        min_amount: int | None = None,
        max_amount: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        description: str | None = None,
        category_id: int | None = None,
        sort_by: SortByOptions | None = None,
        direction: SortDirection | None = None,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)):

    expenses = filter_expenses(id, min_amount, max_amount, start_date, end_date, description, category_id, current_user, db)
    if sort_by:
        expenses = sort_expenses(expenses, sort_by, direction)
    expenses = expenses.all()

    if expenses is None:
        raise HTTPException(status_code=404, detail="There are no expenses")
    return {"expenses": expenses}


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expenses(expense_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == current_user.id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.post("", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    new_expense = Expense(
        amount=expense.amount,
        date=expense.date,
        description=expense.description,
        category_id=expense.category_id,
        user_id=current_user.id
    )
    db.add(new_expense)

    user = db.query(User).filter(User.id == current_user.id).first()
    user.balance -= expense.amount

    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, new_expense: ExpenseCreate, current_user: User = Depends(get_current_active_user),
                   db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    balance_difference = expense.amount - new_expense.amount
    user = db.query(User).filter(User.id == current_user.id).first()
    user.balance += balance_difference

    expense.amount = new_expense.amount
    expense.date = new_expense.date
    expense.description = new_expense.description
    expense.category_id = new_expense.category_id

    db.commit()
    db.refresh(expense)
    return expense


@router.delete('/{expense_id}')
def delete_expense(expense_id: int, current_user: User = Depends(get_current_active_user),
                   db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted"}


@router.get("/stats/{aggregation}", response_model=Dict[str, float | str])
def get_expense_aggregations(
        aggregation: AggregationType,
        id: int | None = None,
        min_amount: int | None = None,
        max_amount: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        description: str | None = None,
        category_id: int | None = None,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)):

    aggregated_expenses = aggregate_expenses(aggregation, db)
    aggregated_expenses = filter_expenses(id, min_amount, max_amount, start_date, end_date, description, category_id, current_user, db, aggregated_expenses)
    aggregated_expenses = aggregated_expenses.scalar()

    if aggregated_expenses is None:
        aggregated_expenses = 0

    return {str(aggregation.value): aggregated_expenses}


# @router.get('/stats')
# def stats(period: Optional[str] = Query('month'), db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
#     # basic aggregation: total spent in period. 'month'|'quarter'|'year'
#     now = datetime.utcnow()
#     if period == 'month':
#         start = datetime(now.year, now.month, 1)
#     elif period == 'year':
#         start = datetime(now.year, 1, 1)
#     elif period == 'quarter':
#         q = (now.month - 1) // 3
#         start = datetime(now.year, q*3 + 1, 1)
#     else:
#         start = datetime(1970,1,1)
#     total_spent = db.query(func.coalesce(func.sum(models.Expense.amount), 0.0)).filter(models.Expense.user_id == user.id, models.Expense.date >= start).scalar()
#     return {"period": period, "from": start.isoformat(), "total_spent": float(total_spent), "balance": float(user.balance)}
