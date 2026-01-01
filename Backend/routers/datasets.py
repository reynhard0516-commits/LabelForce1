from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from models import Dataset, DataItem, User
from auth import decode_token

router = APIRouter(
    prefix="/datasets",
    tags=["datasets"]
)

# =====================================================
# SCHEMAS
# =====================================================

class DatasetCreate(BaseModel):
    name: str
    description: str | None = None


class DataItemCreate(BaseModel):
    data_type: str
    data_url: str


# =====================================================
# DATASET ROUTES
# =====================================================

@router.post("/")
async def create_dataset(
    data: DatasetCreate,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token.get("sub")

    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one()

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
        "description": dataset.description
    }


@router.get("/")
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

    return [
        {
            "id": d.id,
            "name": d.name,
            "description": d.description
        }
        for d in datasets
    ]


# =====================================================
# DATA ITEM ROUTE
# =====================================================

@router.post("/{dataset_id}/items")
async def add_item(
    dataset_id: int,
    data: DataItemCreate,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Dataset).where(Dataset.id == dataset_id)
    )
    dataset = result.scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    item = DataItem(
        dataset_id=dataset.id,
        data_type=data.data_type,
        data_url=data.data_url
    )

    session.add(item)
    await session.commit()

    return {"message": "Item added"}
