from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, Query
from sqlalchemy.sql import func
from datetime import datetime
from app.models import User, Expense
from app.database import SessionLocal
from app.auth_utils import oauth2_scheme, verify_token
from app.schemas.expense import SortByOptions, SortDirection, AggregationType


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_data = verify_token(token)
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user



def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(
            status_code=404,
            detail="Inactive User",
        )
    return current_user


def filter_expenses(
        id: int | None = None,
        min_amount: int | None = None,
        max_amount: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        description: str | None = None,
        category_id: int | None = None,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
        expenses: Query = None):

    filter_params = []
    if id: filter_params.append(Expense.id == id)
    if min_amount: filter_params.append(Expense.amount >= min_amount)
    if max_amount: filter_params.append(Expense.amount <= max_amount)
    if start_date: filter_params.append(Expense.date >= start_date)
    if end_date: filter_params.append(Expense.date <= end_date)
    if category_id: filter_params.append(Expense.category_id == category_id)
    if description: filter_params.append(Expense.description.contains(description))

    if expenses is None:
        expenses = db.query(Expense)

    expenses = expenses.filter(Expense.user_id == current_user.id, *filter_params)

    return expenses


def sort_expenses(
        expenses: Query,
        sort_by: SortByOptions,
        direction: SortDirection | None = None):

    match sort_by:
        case SortByOptions.id:
            column = Expense.id
        case SortByOptions.amount:
            column = Expense.amount
        case SortByOptions.date:
            column = Expense.date
        case SortByOptions.description:
            column = Expense.description
        case SortByOptions.category_id:
            column = Expense.category_id

    if direction == SortDirection.desc:
        column = column.desc()
    else:
        column = column.asc()

    expenses = expenses.order_by(column)

    return expenses


def aggregate_expenses(aggregation: AggregationType, db: Session):

    match aggregation:
        case AggregationType.sum:
            expenses = db.query(func.sum(Expense.amount).label("Total expenses"))
        case AggregationType.avg:
            expenses = db.query(func.avg(Expense.amount).label("Average expense amount"))
        case AggregationType.min:
            expenses = db.query(func.min(Expense.amount).label("Minimum expense amount"))
        case AggregationType.max:
            expenses = db.query(func.max(Expense.amount).label("Maximum expense amount"))
        case AggregationType.count:
            expenses = db.query(func.count(Expense.amount).label("Number of expenses"))

    return expenses
