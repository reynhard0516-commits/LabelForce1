from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from models import Label, Dataset, User
from auth import decode_token

router = APIRouter(
    prefix="/datasets/{dataset_id}/labels",
    tags=["labels"]
)

class LabelCreate(BaseModel):
    name: str
    color: str | None = None


@router.post("")
async def create_label(
    dataset_id: int,
    data: LabelCreate,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token["sub"]

    user = (
        await session.execute(
            select(User).where(User.email == email)
        )
    ).scalar_one()

    dataset = (
        await session.execute(
            select(Dataset).where(Dataset.id == dataset_id)
        )
    ).scalar_one_or_none()

    if not dataset or dataset.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Dataset not found")

    label = Label(
        name=data.name,
        color=data.color,
        dataset_id=dataset_id
    )

    session.add(label)
    await session.commit()
    await session.refresh(label)

    return label


@router.get("")
async def list_labels(
    dataset_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    await decode_token(token)

    result = await session.execute(
        select(Label).where(Label.dataset_id == dataset_id)
    )
    return result.scalars().all()
