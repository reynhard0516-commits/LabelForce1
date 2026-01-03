from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.dataset import Dataset

router = APIRouter(prefix="/datasets", tags=["datasets"])


def get_user_id(authorization: str | None):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return int(authorization.replace("Bearer ", ""))


@router.get("/")
async def get_datasets(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db),
):
    user_id = get_user_id(authorization)
    result = await db.execute(select(Dataset).where(Dataset.owner_id == user_id))
    return result.scalars().all()


@router.post("/")
async def create_dataset(
    name: str,
    description: str | None = None,
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db),
):
    user_id = get_user_id(authorization)

    dataset = Dataset(
        name=name,
        description=description,
        owner_id=user_id,
    )

    db.add(dataset)
    await db.commit()
    await db.refresh(dataset)
    return dataset
