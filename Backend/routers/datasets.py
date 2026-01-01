from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from models import Dataset, User
from auth import decode_token

router = APIRouter(
    prefix="/datasets",
    tags=["datasets"]
)

# =====================================================
# Schemas
# =====================================================

class DatasetCreate(BaseModel):
    name: str
    description: str | None = None


class DatasetOut(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int

    class Config:
        from_attributes = True


# =====================================================
# Create Dataset
# =====================================================

@router.post("/", response_model=DatasetOut)
async def create_dataset(
    data: DatasetCreate,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    dataset = Dataset(
        name=data.name,
        description=data.description,
        owner_id=user.id
    )

    session.add(dataset)
    await session.commit()
    await session.refresh(dataset)

    return dataset


# =====================================================
# List My Datasets
# =====================================================

@router.get("/", response_model=list[DatasetOut])
async def list_datasets(
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await session.execute(
        select(Dataset).where(Dataset.owner_id == user.id)
    )

    return result.scalars().all()


# =====================================================
# Get Single Dataset (OWNER ONLY)
# =====================================================

@router.get("/{dataset_id}", response_model=DatasetOut)
async def get_dataset(
    dataset_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await session.execute(
        select(Dataset).where(
            Dataset.id == dataset_id,
            Dataset.owner_id == user.id
        )
    )
    dataset = result.scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return dataset
