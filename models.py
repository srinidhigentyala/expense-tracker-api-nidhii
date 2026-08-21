from sqlalchemy import Column,Integer, String
from database import Base

class Expense(Base):
    __tablename__ = "Expense_Tracker"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    amount = Column(Integer)
    category = Column(String,default = "food")
    date = Column(String,default="2026-08-19")

class Budget(Base):
    __tablename__ = "Monthly_Budget"

    id = Column(Integer,primary_key =True, index = True)
    budget_amount = Column(Integer)
    total_spent = Column(Integer)
    remaining_amt = Column(Integer)
    month = Column(String)