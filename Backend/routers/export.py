from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from models import Dataset, DataItem, Label, Annotation
from auth import decode_token

router = APIRouter(
    prefix="/export",
    tags=["export"]
)

@router.get("/{dataset_id}")
async def export_dataset(
    dataset_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    # Check dataset
    result = await session.execute(
        select(Dataset).where(Dataset.id == dataset_id)
    )
    dataset = result.scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Fetch related data
    items = (await session.execute(
        select(DataItem).where(DataItem.dataset_id == dataset_id)
    )).scalars().all()

    labels = (await session.execute(
        select(Label).where(Label.dataset_id == dataset_id)
    )).scalars().all()

    annotations = (await session.execute(
        select(Annotation)
        .join(DataItem)
        .where(DataItem.dataset_id == dataset_id)
    )).scalars().all()

    return {
        "dataset": {
            "id": dataset.id,
            "name": dataset.name,
            "description": dataset.description,
        },
        "labels": [
            {
                "id": l.id,
                "name": l.name,
                "color": l.color,
            } for l in labels
        ],
        "items": [
            {
                "id": i.id,
                "type": i.data_type,
                "data": i.data_url,
            } for i in items
        ],
        "annotations": [
            {
                "id": a.id,
                "item_id": a.item_id,
                "label_id": a.label_id,
                "data": a.data,
            } for a in annotations
        ]
    }
