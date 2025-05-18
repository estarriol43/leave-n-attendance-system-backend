import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/postgres")
    JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")
    print("DATABASE_URL =", os.getenv("DATABASE_URL"))


settings = Settings()
