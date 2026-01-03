from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import io
import zipfile
import json
import os

from database import get_db
from auth import decode_token
from models import Dataset, DataItem, Label, Annotation, User

router = APIRouter(prefix="/export", tags=["export"])


# =====================================================
# RAW EXPORT
# =====================================================
@router.get("/{dataset_id}")
async def export_raw(
    dataset_id: int,
    token=Depends(decode_token),
    db: AsyncSession = Depends(get_db),
):
    email = token["sub"]

    user = (
        await db.execute(select(User).where(User.email == email))
    ).scalar_one()

    dataset = (
        await db.execute(
            select(Dataset).where(
                Dataset.id == dataset_id,
                Dataset.owner_id == user.id
            )
        )
    ).scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    items = (
        await db.execute(select(DataItem).where(DataItem.dataset_id == dataset_id))
    ).scalars().all()

    labels = (
        await db.execute(select(Label).where(Label.dataset_id == dataset_id))
    ).scalars().all()

    annotations = (
        await db.execute(
            select(Annotation)
            .join(DataItem)
            .where(DataItem.dataset_id == dataset_id)
        )
    ).scalars().all()

    return {
        "dataset": {
            "id": dataset.id,
            "name": dataset.name,
            "description": dataset.description,
        },
        "labels": [{"id": l.id, "name": l.name, "color": l.color} for l in labels],
        "items": [{"id": i.id, "type": i.data_type, "data": i.data_url} for i in items],
        "annotations": [
            {
                "id": a.id,
                "item_id": a.item_id,
                "label_id": a.label_id,
                "data": a.data,
            }
            for a in annotations
        ],
    }


# =====================================================
# COCO EXPORT
# =====================================================
@router.get("/coco/{dataset_id}")
async def export_coco(
    dataset_id: int,
    token=Depends(decode_token),
    db: AsyncSession = Depends(get_db),
):
    email = token["sub"]

    user = (
        await db.execute(select(User).where(User.email == email))
    ).scalar_one()

    dataset = (
        await db.execute(
            select(Dataset).where(
                Dataset.id == dataset_id,
                Dataset.owner_id == user.id
            )
        )
    ).scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    labels = (
        await db.execute(select(Label).where(Label.dataset_id == dataset_id))
    ).scalars().all()

    items = (
        await db.execute(
            select(DataItem).where(
                DataItem.dataset_id == dataset_id,
                DataItem.data_type == "image"
            )
        )
    ).scalars().all()

    annotations = (
        await db.execute(
            select(Annotation)
            .join(DataItem)
            .where(DataItem.dataset_id == dataset_id)
        )
    ).scalars().all()

    coco = {"images": [], "annotations": [], "categories": []}

    label_map = {l.id: i + 1 for i, l in enumerate(labels)}
    for l in labels:
        coco["categories"].append({
            "id": label_map[l.id],
            "name": l.name,
        })

    image_map = {i.id: idx + 1 for idx, i in enumerate(items)}
    for i in items:
        coco["images"].append({
            "id": image_map[i.id],
            "file_name": i.data_url,
        })

    ann_id = 1
    for a in annotations:
        if a.item_id not in image_map:
            continue

        box = a.data.get("box") if a.data else None
        if not box:
            continue

        coco["annotations"].append({
            "id": ann_id,
            "image_id": image_map[a.item_id],
            "category_id": label_map[a.label_id],
            "bbox": [box["x"], box["y"], box["width"], box["height"]],
            "area": box["width"] * box["height"],
            "iscrowd": 0,
        })
        ann_id += 1

    return coco


# =====================================================
# YOLO EXPORT
# =====================================================
@router.get("/yolo/{dataset_id}")
async def export_yolo(
    dataset_id: int,
    token=Depends(decode_token),
    db: AsyncSession = Depends(get_db),
):
    labels = (
        await db.execute(select(Label).where(Label.dataset_id == dataset_id))
    ).scalars().all()

    label_index = {l.id: i for i, l in enumerate(labels)}

    items = (
        await db.execute(
            select(DataItem).where(
                DataItem.dataset_id == dataset_id,
                DataItem.data_type == "image"
            )
        )
    ).scalars().all()

    annotations = (
        await db.execute(
            select(Annotation)
            .join(DataItem)
            .where(DataItem.dataset_id == dataset_id)
        )
    ).scalars().all()

    yolo = {}

    for a in annotations:
        box = a.data.get("box") if a.data else None
        if not box:
            continue

        item = next((i for i in items if i.id == a.item_id), None)
        if not item:
            continue

        x = box["x"] + box["width"] / 2
        y = box["y"] + box["height"] / 2

        line = f"{label_index[a.label_id]} {x} {y} {box['width']} {box['height']}"
        yolo.setdefault(item.data_url, []).append(line)

    return yolo
