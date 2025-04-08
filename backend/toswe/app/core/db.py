from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings
# import os
from dotenv import load_dotenv

load_dotenv()

# Remplace les valeurs par celles de ta configuration
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://sam:1100111postgresql@localhost:5432/toswe_db")

engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
