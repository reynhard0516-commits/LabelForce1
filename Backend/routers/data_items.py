import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from models import DataItem, Dataset, User
from auth import decode_token

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(
    prefix="/datasets/{dataset_id}/items",
    tags=["data-items"]
)

# ============================
# Create TEXT item
# ============================

@router.post("/text")
async def create_text_item(
    dataset_id: int,
    text: str,
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

    item = DataItem(
        dataset_id=dataset_id,
        data_type="text",
        data_url=text
    )

    session.add(item)
    await session.commit()
    await session.refresh(item)

    return item


# ============================
# Create IMAGE item
# ============================

@router.post("/image")
async def create_image_item(
    dataset_id: int,
    file: UploadFile = File(...),
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

    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    item = DataItem(
        dataset_id=dataset_id,
        data_type="image",
        data_url=f"/uploads/{filename}"
    )

    session.add(item)
    await session.commit()
    await session.refresh(item)

    return item


# ============================
# List items
# ============================

@router.get("")
async def list_items(
    dataset_id: int,
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

    result = await session.execute(
        select(DataItem).where(DataItem.dataset_id == dataset_id)
    )

    return result.scalars().all()
