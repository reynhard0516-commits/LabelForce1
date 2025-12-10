# Backend/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "change_me_secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    RESET_DB: bool = False  # set to "true" in Render to drop and recreate tables once

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
