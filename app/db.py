import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please configure it in your .env file or environment. "
        "Example: postgresql://user:password@localhost:5432/fitforge"
    )

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    echo=True if os.getenv("DEBUG") == "true" else False
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for models using SQLAlchemy 2.0 style
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models"""
    pass


# Dependency to get database session
def get_db():
    """
    Database session dependency for FastAPI routes.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all database tables defined in models.
    This should be called once during initial setup.
    """
    from app.models import User, Exercise, Workout, Run, Plan  # Import models to register them
    Base.metadata.create_all(bind=engine)
    print("✅ All database tables created successfully!")


def drop_tables():
    """
    Drop all database tables. Use with caution!
    Only for development/testing purposes.
    """
    from app.models import User, Exercise, Workout, Run, Plan
    Base.metadata.drop_all(bind=engine)
    print("⚠️  All database tables dropped!")