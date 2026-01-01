from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from models import Annotation, DataItem, Label, Dataset, User
from auth import decode_token

router = APIRouter(
    prefix="/annotations",
    tags=["annotations"]
)

# =====================================================
# Schemas
# =====================================================

class AnnotationCreate(BaseModel):
    item_id: int
    label_id: int
    value: str  # bbox, polygon, text, JSON string


class AnnotationOut(BaseModel):
    id: int
    item_id: int
    label_id: int
    user_id: int
    value: str

    class Config:
        from_attributes = True


# =====================================================
# Create Annotation (label an item)
# =====================================================

@router.post("/", response_model=AnnotationOut)
async def create_annotation(
    data: AnnotationCreate,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Get user
    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get item
    result = await session.execute(
        select(DataItem).where(DataItem.id == data.item_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Data item not found")

    # Get dataset (via item)
    result = await session.execute(
        select(Dataset).where(Dataset.id == item.dataset_id)
    )
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Get label
    result = await session.execute(
        select(Label).where(
            Label.id == data.label_id,
            Label.dataset_id == dataset.id
        )
    )
    label = result.scalar_one_or_none()
    if not label:
        raise HTTPException(status_code=404, detail="Label not found for this dataset")

    annotation = Annotation(
        item_id=item.id,
        label_id=label.id,
        user_id=user.id,
        value=data.value
    )

    session.add(annotation)
    await session.commit()
    await session.refresh(annotation)

    return annotation


# =====================================================
# List Annotations for Item
# =====================================================

@router.get("/item/{item_id}", response_model=list[AnnotationOut])
async def list_annotations_for_item(
    item_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token.get("sub")

    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await session.execute(
        select(Annotation).where(Annotation.item_id == item_id)
    )
    return result.scalars().all()


# =====================================================
# Delete Annotation (owner only)
# =====================================================

@router.delete("/{annotation_id}")
async def delete_annotation(
    annotation_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token.get("sub")

    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await session.execute(
        select(Annotation).where(
            Annotation.id == annotation_id,
            Annotation.user_id == user.id
        )
    )
    annotation = result.scalar_one_or_none()

    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")

    await session.delete(annotation)
    await session.commit()

    return {"message": "Annotation deleted"}
