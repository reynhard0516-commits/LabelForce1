from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.label import Label

router = APIRouter(prefix="/labels", tags=["labels"])


def get_user_id(auth: str | None):
    if not auth:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return int(auth.replace("Bearer ", ""))


@router.get("/{dataset_id}")
async def get_labels(
    dataset_id: int,
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(select(Label).where(Label.dataset_id == dataset_id))
    return res.scalars().all()


@router.post("/{dataset_id}")
async def create_label(
    dataset_id: int,
    name: str,
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db),
):
    get_user_id(authorization)

    label = Label(name=name, dataset_id=dataset_id)
    db.add(label)
    await db.commit()
    await db.refresh(label)
    return label
