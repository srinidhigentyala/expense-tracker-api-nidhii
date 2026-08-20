from fastapi import FastAPI, HTTPException,Depends
from sqlalchemy.orm import Session
import models
from schemas import Expenses
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db() :
    try :
        db = SessionLocal()
        yield db
    finally :
        db.close()


# POST - Create Task 
@app.post("/expenses")
def create_expense(expense : Expenses,db : Session = Depends(get_db)):
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