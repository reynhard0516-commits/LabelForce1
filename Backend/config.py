from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./database.db"
    SECRET_KEY: str = "super-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()
