from fastapi import FastAPI, HTTPException,Depends
from sqlalchemy.orm import Session
import models
from schemas import ExpenseCreate, UpdateExpense,BudgetCreate
from database import engine, SessionLocal

app = FastAPI(title= "Personal Expense Tracker API")

models.Base.metadata.create_all(bind=engine)

def get_db() :
    try :
        db = SessionLocal()
        yield db
    finally :
        db.close()


# POST - Create Task 
@app.post("/expenses")
def create_expense(expense : ExpenseCreate,db : Session = Depends(get_db)):
    new_expense = models.Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category,
        date=expense.date
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return {
        "id" : new_expense.id,
        "message" : "Expense recorded",
        "expense" : new_expense
    }

# GET - List all expenses
@app.get("/expenses")
def get_expenses(db : Session = Depends(get_db)):
    expenses = db.query(models.Expense).all()
    if expenses is None :
        raise HTTPException (
            status_code =404,
            detail = "No Expenses Found"
        )
    db.close()
    return expenses

# GET - Get one expense by Id (404 if not found)
@app.get("/expenses/{expense_id}")
def get_expense(expense_id :int, db : Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense :
        raise HTTPException (
            status_code = 404,
            detail = "Id not found"
        )
    return expense

# PUT - Update an expense
@app.put("/expenses/{expense_id}")
def update_expense(expense_id : int,updated_expense : UpdateExpense, db : Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if expense is None :
        raise HTTPException (
            status_code = 404,
            detail = "Expense not found to Update"
        )
    expense.title = updated_expense.title
    expense.amount = updated_expense.amount
    expense.category = updated_expense.category
    expense.date = updated_expense.date
    db.commit()
    db.refresh(expense)
    db.close()
    return {
        "message" : "Expense Updated Successfully",
        "expense" : expense
    }

# DELETE - delete an expense
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id : int,db : Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense :
        raise HTTPException(
            status_code = 404,
            detail = "Expense not found"
        )
    db.delete(expense)
    db.commit()
    db.close()
    return {
        "message" : f"Expense with id, {expense_id} is deleted successfully"
    }

# GET - get all expenses by category
@app.get("/expenses/category/{category}")
def get_all_expenses(category : str, db:Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.category == category).all()
    if not expense :
        raise HTTPException(
            status_code = 404,
            detail = "Expenses not available with this category"
        )
    db.close()
    return expense

# GET - get all expenses on given date
@app.get("/expenses/date/{date}")
def get_all_expenses_by_date(date : str, db : Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.date == date).all()
    if not expense :
        raise HTTPException (
            status_code = 404,
            detail = "Invalid date or Expenses not available with this date"
        )
    db.close()
    return expense

# POST - set a monthly budget
@app.post("/budget")
def monthly_budget(budget:BudgetCreate, db:Session = Depends(get_db)):
    new_budget = models.Budget(
        budget_amount = budget.budget_amount,
        total_spent = budget.total_spent,
        remaining_amt = budget.remaining_amt,
        month = budget.month
    )
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return {
        "id" : new_budget.id,
        "message" : "Budget_Added",
        "budget" : new_budget
    }
