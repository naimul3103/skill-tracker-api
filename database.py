# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file
# "check_same_thread=False" is required for SQLite with FastAPI
SQLALCHEMY_DATABASE_URL = "sqlite:///./skill_tracker.db"

# Create the engine (the connection to the database file)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite-specific
)

# Create a session factory
# Each call to SessionLocal() creates a NEW session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


# THE DEPENDENCY: Provides a session to each endpoint
def get_db():
    """
    Dependency that provides a database session.
    
    SETUP:   Create session
    YIELD:   Pass session to endpoint
    CLEANUP: Close session (always runs, even on error)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()