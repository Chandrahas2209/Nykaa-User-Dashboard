from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
# SQLite DB URL
DATABASE_URL = "sqlite:///./users.db"
# SQLAlchemy engine with SQLite-specific connection config
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
# Session manager
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base class for ORM models
Base = declarative_base()
