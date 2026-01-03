from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from models import DataItem, Dataset, User
from auth import decode_token

router = APIRouter(
    prefix="/datasets/{dataset_id}/items",
    tags=["data-items"]
)

# ============================
# Schemas
# ============================

class DataItemCreate(BaseModel):
    data_type: str  # "text" or "image"
    data_value: str  # text content or image URL


# ============================
# Create item
# ============================

@router.post("")
async def create_item(
    dataset_id: int,
    data: DataItemCreate,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token.get("sub")

    # Get user
    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    # Get dataset
    result = await session.execute(
        select(Dataset).where(Dataset.id == dataset_id)
    )
    dataset = result.scalar_one_or_none()

    if not dataset or dataset.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Dataset not found")

    item = DataItem(
        dataset_id=dataset_id,
        data_type=data.data_type,
        data_url=data.data_value
    )

    session.add(item)
    await session.commit()
    await session.refresh(item)

    return item


# ============================
# List items
# ============================

@router.get("")
async def list_items(
    dataset_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token.get("sub")

    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one()

    result = await session.execute(
        select(Dataset).where(Dataset.id == dataset_id)
    )
    dataset = result.scalar_one_or_none()

    if not dataset or dataset.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Dataset not found")

    result = await session.execute(
        select(DataItem).where(DataItem.dataset_id == dataset_id)
    )

    return result.scalars().all()
