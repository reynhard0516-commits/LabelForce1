from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from models import Annotation, DataItem, Label, User
from auth import decode_token

router = APIRouter(
    prefix="/items/{item_id}/annotations",
    tags=["annotations"]
)

class AnnotationCreate(BaseModel):
    label_id: int
    value: str


@router.post("")
async def create_annotation(
    item_id: int,
    data: AnnotationCreate,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token["sub"]

    user = (
        await session.execute(
            select(User).where(User.email == email)
        )
    ).scalar_one()

    item = (
        await session.execute(
            select(DataItem).where(DataItem.id == item_id)
        )
    ).scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    label = (
        await session.execute(
            select(Label).where(Label.id == data.label_id)
        )
    ).scalar_one_or_none()

    if not label:
        raise HTTPException(status_code=404, detail="Label not found")

    annotation = Annotation(
        item_id=item_id,
        user_id=user.id,
        label_id=label.id,
        value=data.value
    )

    session.add(annotation)
    await session.commit()
    await session.refresh(annotation)

    return annotation


@router.get("")
async def list_annotations(
    item_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    await decode_token(token)

    result = await session.execute(
        select(Annotation).where(Annotation.item_id == item_id)
    )
    return result.scalars().all()
