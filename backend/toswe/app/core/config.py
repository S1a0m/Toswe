# app/config.py
import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 jours
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://sam:1100111postgresql@localhost:5432/toswe_db")


settings = Settings()
