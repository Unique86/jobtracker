from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = "sqlite:///./jobtracker.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

print("Current working directory:", os.getcwd())
print("Database URL:", DATABASE_URL)
print("Database absolute path:", os.path.abspath("jobtracker.db"))

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()