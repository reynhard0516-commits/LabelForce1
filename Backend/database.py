from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Load database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Async engine
engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False
)

# Base model
Base = declarative_base()

# Session factory
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


# Dependency for FastAPI routes
async def some_route(session: AsyncSession = Depends(get_session)):
