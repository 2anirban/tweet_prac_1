# ### 1.3 Database Setup ([database.py](Backend/database.py))
# - [ ] Set up SQLAlchemy engine
# - [ ] Create SessionLocal for database sessions
# - [ ] Create Base class for models
# - [ ] Implement `get_db()` dependency for FastAPI

# ---
from sqlalchemy import create_engine
#Create a connection to the database
from sqlalchemy.ext.declarative import declarative_base
#Factory Function that creates a base class for your ORM models
from sqlalchemy.orm import sessionmaker
#Factory for creating database session objects
from config import settings
# Import the settings instance (not the class)


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # Only for SQLite
)

Base= declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()