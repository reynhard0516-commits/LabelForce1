from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from models import Dataset
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


# =====================================================
# Create Dataset
# =====================================================

@router.post("")
async def create_dataset(
    data: DatasetCreate,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Find user
    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create dataset WITH owner_id
    dataset = Dataset(
        name=data.name,
        description=data.description,
        owner_id=user.id
    )

    session.add(dataset)
    await session.commit()
    await session.refresh(dataset)

    return {
        "id": dataset.id,
        "name": dataset.name,
        "description": dataset.description,
        "owner_id": dataset.owner_id
    }

# =====================================================
# List My Datasets
# =====================================================

@router.get("")
async def list_datasets(
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token.get("sub")

    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one()

    result = await session.execute(
        select(Dataset).where(Dataset.owner_id == user.id)
    )
    datasets = result.scalars().all()

    return datasets


# =====================================================
# Get Single Dataset
# =====================================================

@router.get("/{dataset_id}")
async def get_dataset(
    dataset_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Dataset).where(Dataset.id == dataset_id)
    )
    dataset = result.scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return dataset
