from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    amount: float
    date: datetime
    description: str
    category_id: int



class ExpenseResponse(BaseModel):
    id: int
    amount: float
    date: datetime
    description: str
    category_id: int

    class Config:
        orm_mode = True


class SortByOptions(str, Enum):
    id = "id"
    amount = "amount"
    date = "date"
    description = "description"
    category_id = "category_id"


class SortDirection(str, Enum):
    asc = "asc"
    desc = "desc"


class AggregationType(str, Enum):
    sum = "sum"
    avg = "avg"
    min = "min"
    max = "max"
    count = "count"
