import os
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase

# =====================================================
# DATABASE URL
# =====================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./labelforce.db"  # fallback for local dev
)

# =====================================================
# ENGINE
# =====================================================

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

# =====================================================
# SESSION
# =====================================================

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

# =====================================================
# BASE
# =====================================================

class Base(DeclarativeBase):
    pass

# =====================================================
# DEPENDENCY
# =====================================================

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
