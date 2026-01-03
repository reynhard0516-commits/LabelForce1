from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from Backend.database import get_db
from Backend.models.dataset import Dataset

router = APIRouter(prefix="/datasets", tags=["datasets"])


def get_current_user_id(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return int(authorization.replace("Bearer ", ""))


@router.get("/")
async def list_datasets(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Dataset).where(Dataset.owner_id == user_id)
    )
    return result.scalars().all()


@router.post("/")
async def create_dataset(
    name: str,
    description: str = "",
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    dataset = Dataset(
        name=name,
        description=description,
        owner_id=user_id,
    )

    db.add(dataset)
    await db.commit()
    await db.refresh(dataset)

    return dataset
