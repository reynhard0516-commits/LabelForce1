from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Your actual Render database URL (asyncpg required!)
    DATABASE_URL: str = (
        "postgresql+asyncpg://new_tqnu_user:rI1OwOD7nlcgdQNvoypevvgcT3COzTfz"
        "@dpg-d4shhrmmcj7s73c0fht0-a.oregon-postgres.render.com/new_tqnu"
        "?sslmode=require"
    )

    SECRET_KEY: str = "change_me_secret"   # change this later in Render
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days token lifetime

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
