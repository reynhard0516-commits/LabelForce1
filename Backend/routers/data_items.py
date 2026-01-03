from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from models.data_item import DataItem
from models.dataset import Dataset
from schemas.data_item import DataItemCreate, DataItemOut
from auth.dependencies import get_current_user

router = APIRouter(prefix="/datasets/{dataset_id}/items", tags=["data items"])

@router.get("/", response_model=list[DataItemOut])
async def list_items(
    dataset_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    result = await db.execute(
        select(DataItem).where(DataItem.dataset_id == dataset_id)
    )
    return result.scalars().all()

@router.post("/", response_model=DataItemOut)
async def create_item(
    dataset_id: int,
    item: DataItemCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    # ensure dataset exists and belongs to user
    result = await db.execute(
        select(Dataset).where(
            Dataset.id == dataset_id,
            Dataset.owner_id == user.id
        )
    )
    dataset = result.scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    db_item = DataItem(
        dataset_id=dataset_id,
        content=item.content,
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)

    return db_item
