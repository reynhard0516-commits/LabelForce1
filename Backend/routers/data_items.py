from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from models.data_item import DataItem

router = APIRouter(prefix="/items", tags=["items"])


def get_user_id(authorization: str | None):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return int(authorization.replace("Bearer ", ""))


@router.get("/{dataset_id}")
async def get_items(
    dataset_id: int,
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db),
):
    get_user_id(authorization)

    result = await db.execute(
        select(DataItem).where(DataItem.dataset_id == dataset_id)
    )
    return result.scalars().all()


@router.post("/{dataset_id}")
async def create_item(
    dataset_id: int,
    data_type: str,
    data_url: str,
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db),
):
    user_id = get_user_id(authorization)

    item = DataItem(
        dataset_id=dataset_id,
        data_type=data_type,
        data_url=data_url,
        owner_id=user_id,
    )

    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item
