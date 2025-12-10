from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "change-me-in-render"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = str(Path(__file__).parent / ".env")
        case_sensitive = True

settings = Settings()
