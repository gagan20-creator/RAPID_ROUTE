# File: ride_request_app/server/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- Database Configuration ---
# Replace 'your_user' and 'your_password' with your actual PostgreSQL credentials.
DATABASE_URL = "postgresql://postgres:gun1@localhost/ride_db"

# The engine is the entry point to the database.
# It handles the connection and communication.
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory for creating new database sessions.
# Each session is a single unit of work with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is a base class for our ORM models.
# All our database table models will inherit from this class.
Base = declarative_base()