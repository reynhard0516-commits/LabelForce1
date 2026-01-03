from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from database import get_session
from models import DataItem, Dataset, User
from auth import decode_token

router = APIRouter(
    prefix="/datasets/{dataset_id}/items",
    tags=["data_items"]
)

# =========================
# Schemas
# =========================

class DataItemCreate(BaseModel):
    data_type: str   # image, text, video
    data_url: str

# =========================
# List items in dataset
# =========================

@router.get("")
async def list_items(
    dataset_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session),
):
    email = token["sub"]

    user = (
        await session.execute(select(User).where(User.email == email))
    ).scalar_one()

    dataset = (
        await session.execute(
            select(Dataset).where(
                Dataset.id == dataset_id,
                Dataset.owner_id == user.id
            )
        )
    ).scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    result = await session.execute(
        select(DataItem).where(DataItem.dataset_id == dataset_id)
    )

    return result.scalars().all()

# =========================
# Create item
# =========================

@router.post("")
async def create_item(
    dataset_id: int,
    data: DataItemCreate,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session),
):
    email = token["sub"]

    user = (
        await session.execute(select(User).where(User.email == email))
    ).scalar_one()

    dataset = (
        await session.execute(
            select(Dataset).where(
                Dataset.id == dataset_id,
                Dataset.owner_id == user.id
            )
        )
    ).scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    item = DataItem(
        dataset_id=dataset_id,
        data_type=data.data_type,
        data_url=data.data_url,
    )

    session.add(item)
    await session.commit()
    await session.refresh(item)

    return item
