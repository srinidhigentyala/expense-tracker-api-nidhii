from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str = "food"
    date: str = "2026-08-19"


class UpdateExpense(ExpenseCreate):
    title: str
    amount: float
    category: str = "food"
    date: str = "2026-08-19"