from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from models import Dataset, DataItem, User
from auth import decode_token

router = APIRouter(
    prefix="/datasets",
    tags=["data-items"]
)

# =====================================================
# Schemas
# =====================================================

class DataItemCreate(BaseModel):
    data_type: str     # image, text, video
    data_url: str      # URL or path


class DataItemOut(BaseModel):
    id: int
    dataset_id: int
    data_type: str
    data_url: str

    class Config:
        from_attributes = True


# =====================================================
# Add Item to Dataset
# =====================================================

@router.post("/{dataset_id}/items", response_model=DataItemOut)
async def add_item_to_dataset(
    dataset_id: int,
    data: DataItemCreate,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Get user
    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check dataset ownership
    result = await session.execute(
        select(Dataset).where(
            Dataset.id == dataset_id,
            Dataset.owner_id == user.id
        )
    )
    dataset = result.scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    item = DataItem(
        dataset_id=dataset_id,
        data_type=data.data_type,
        data_url=data.data_url
    )

    session.add(item)
    await session.commit()
    await session.refresh(item)

    return item


# =====================================================
# List Items in Dataset
# =====================================================

@router.get("/{dataset_id}/items", response_model=list[DataItemOut])
async def list_dataset_items(
    dataset_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token.get("sub")

    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify dataset ownership
    result = await session.execute(
        select(Dataset).where(
            Dataset.id == dataset_id,
            Dataset.owner_id == user.id
        )
    )
    dataset = result.scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    result = await session.execute(
        select(DataItem).where(DataItem.dataset_id == dataset_id)
    )

    return result.scalars().all()


# =====================================================
# Get Single Item
# =====================================================

@router.get("/items/{item_id}", response_model=DataItemOut)
async def get_item(
    item_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token.get("sub")

    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await session.execute(
        select(DataItem, Dataset)
        .join(Dataset)
        .where(
            DataItem.id == item_id,
            Dataset.owner_id == user.id
        )
    )

    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")

    item, _ = row
    return item
