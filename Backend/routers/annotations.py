from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.annotation import Annotation

router = APIRouter(prefix="/annotations", tags=["annotations"])


def get_user_id(auth: str | None):
    if not auth:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return int(auth.replace("Bearer ", ""))


@router.get("/{item_id}")
async def get_annotations(
    item_id: int,
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(
        select(Annotation).where(Annotation.data_item_id == item_id)
    )
    return res.scalars().all()


@router.post("/{item_id}")
async def create_annotation(
    item_id: int,
    label_id: int,
    data: dict,
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db),
):
    get_user_id(authorization)

    ann = Annotation(
        data_item_id=item_id,
        label_id=label_id,
        data=data,
    )

    db.add(ann)
    await db.commit()
    await db.refresh(ann)
    return ann
