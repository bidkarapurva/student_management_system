import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Install pymysql as MySQL driver
pymysql.install_as_MySQLdb()

# Database connection URL (use environment variables for security)
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/student_project")

# Create database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
