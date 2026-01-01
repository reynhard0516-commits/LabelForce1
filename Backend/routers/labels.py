from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from models import Label, Dataset
from auth import decode_token

router = APIRouter(
    prefix="/labels",
    tags=["labels"]
)

# =====================================================
# Schemas
# =====================================================

class LabelCreate(BaseModel):
    name: str
    color: str | None = None
    dataset_id: int


# =====================================================
# Create Label (dataset owner only)
# =====================================================

@router.post("")
async def create_label(
    data: LabelCreate,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Ensure dataset exists
    result = await session.execute(
        select(Dataset).where(Dataset.id == data.dataset_id)
    )
    dataset = result.scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    label = Label(
        name=data.name,
        color=data.color,
        dataset_id=data.dataset_id
    )

    session.add(label)
    await session.commit()
    await session.refresh(label)

    return {
        "id": label.id,
        "name": label.name,
        "color": label.color,
        "dataset_id": label.dataset_id
    }


# =====================================================
# List Labels for a Dataset
# =====================================================

@router.get("/dataset/{dataset_id}")
async def list_labels(
    dataset_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Label).where(Label.dataset_id == dataset_id)
    )
    labels = result.scalars().all()

    return labels


# =====================================================
# Delete Label
# =====================================================

@router.delete("/{label_id}")
async def delete_label(
    label_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Label).where(Label.id == label_id)
    )
    label = result.scalar_one_or_none()

    if not label:
        raise HTTPException(status_code=404, detail="Label not found")

    await session.delete(label)
    await session.commit()

    return {"message": "Label deleted"}
