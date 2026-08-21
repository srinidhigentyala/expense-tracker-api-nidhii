from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    title: str
    amount: int
    category: str = "food"
    date: str = "2026-08-19"


class UpdateExpense(ExpenseCreate):
    title: str
    amount: int
    category: str = "food"
    date: str = "2026-08-19"

class BudgetCreate(BaseModel):
    budget_amount : int
    total_spent : int
    remaining_amt : int
    month : str