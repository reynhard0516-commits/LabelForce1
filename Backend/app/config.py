class Settings:
    PROJECT_NAME = "Labelforce Backend"
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALG = "HS256"
    REDIS_URL = os.getenv("REDIS_URL")

settings = Settings()
