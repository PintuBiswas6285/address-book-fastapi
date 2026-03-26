# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database URL
DATABASE_URL = "sqlite:///./address.db"

# Engine creation (SQLite needs check_same_thread=False)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory for DB operations
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base class for ORM models
Base = declarative_base()

