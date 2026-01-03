from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from database import get_session
from models.dataset import Dataset

router = APIRouter(prefix="/datasets", tags=["datasets"])


# -----------------------------
# Simple auth helper (temporary)
# -----------------------------
def get_user_id(authorization: str | None):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")

    token = authorization.replace("Bearer ", "")
    return int(token)  # works with your current frontend


# -----------------------------
# Request schemas
# -----------------------------
class DatasetCreate(BaseModel):
    name: str
    description: str | None = None


# -----------------------------
# Routes
# -----------------------------
@router.get("/")
async def get_datasets(
    authorization: str = Header(None),
    session: AsyncSession = Depends(get_session),
):
    user_id = get_user_id(authorization)

    result = await session.execute(
        select(Dataset).where(Dataset.owner_id == user_id)
    )
    return result.scalars().all()


@router.post("/")
async def create_dataset(
    data: DatasetCreate,
    authorization: str = Header(None),
    session: AsyncSession = Depends(get_session),
):
    user_id = get_user_id(authorization)

    dataset = Dataset(
        name=data.name,
        description=data.description,
        owner_id=user_id,
    )

    session.add(dataset)
    await session.commit()
    await session.refresh(dataset)

    return dataset
