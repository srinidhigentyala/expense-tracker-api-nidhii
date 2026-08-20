from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

URL_DATABASE = "sqlite:///./expense_tracker.db"

engine = create_engine(
    URL_DATABASE,
    connect_args = {"check_same_thread" : False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()