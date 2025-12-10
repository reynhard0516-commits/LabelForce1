import os

DATABASE_URL = os.getenv("DATABASE_URL")
RESET_DB = os.getenv("RESET_DB", "false").lower() in ("true", "1", "yes")
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
