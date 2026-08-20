from pydantic import BaseModel

class Expenses(BaseModel) :
    title : str
    amount : int
    category :str = "food"
    date :str = "2026-08-19"