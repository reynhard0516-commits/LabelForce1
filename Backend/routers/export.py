from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from auth import decode_token
from models import Dataset, DataItem, Label, Annotation, User

router = APIRouter(
    prefix="/export",
    tags=["export"]
)

# =====================================================
# COCO EXPORT
# =====================================================

@router.get("/coco/{dataset_id}")
async def export_coco(
    dataset_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session),
):
    email = token["sub"]

    user = (
        await session.execute(
            select(User).where(User.email == email)
        )
    ).scalar_one()

    dataset = (
        await session.execute(
            select(Dataset).where(
                Dataset.id == dataset_id,
                Dataset.owner_id == user.id
            )
        )
    ).scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    labels = (
        await session.execute(
            select(Label).where(Label.dataset_id == dataset_id)
        )
    ).scalars().all()

    items = (
        await session.execute(
            select(DataItem).where(
                DataItem.dataset_id == dataset_id,
                DataItem.data_type == "image"
            )
        )
    ).scalars().all()

    annotations = (
        await session.execute(
            select(Annotation)
            .join(DataItem)
            .where(DataItem.dataset_id == dataset_id)
        )
    ).scalars().all()

    coco = {
        "images": [],
        "annotations": [],
        "categories": [],
    }

    label_map = {}
    for idx, label in enumerate(labels, start=1):
        label_map[label.id] = idx
        coco["categories"].append({
            "id": idx,
            "name": label.name,
        })

    image_map = {}
    for idx, item in enumerate(items, start=1):
        image_map[item.id] = idx
        coco["images"].append({
            "id": idx,
            "file_name": item.data_url,
        })

    ann_id = 1
    for ann in annotations:
        if ann.item_id not in image_map:
            continue

        box = ann.value.get("box") if ann.value else None
        if not box:
            continue

        coco["annotations"].append({
            "id": ann_id,
            "image_id": image_map[ann.item_id],
            "category_id": label_map[ann.label_id],
            "bbox": [
                box["x"],
                box["y"],
                box["width"],
                box["height"],
            ],
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
    session: AsyncSession = Depends(get_session),
):
    email = token["sub"]

    user = (
        await session.execute(
            select(User).where(User.email == email)
        )
    ).scalar_one()

    labels = (
        await session.execute(
            select(Label).where(Label.dataset_id == dataset_id)
        )
    ).scalars().all()

    label_index = {label.id: i for i, label in enumerate(labels)}

    items = (
        await session.execute(
            select(DataItem).where(
                DataItem.dataset_id == dataset_id,
                DataItem.data_type == "image"
            )
        )
    ).scalars().all()

    annotations = (
        await session.execute(
            select(Annotation)
            .join(DataItem)
            .where(DataItem.dataset_id == dataset_id)
        )
    ).scalars().all()

    yolo = {}

    for ann in annotations:
        box = ann.value.get("box") if ann.value else None
        if not box:
            continue

        item = next((i for i in items if i.id == ann.item_id), None)
        if not item:
            continue

        x_center = box["x"] + box["width"] / 2
        y_center = box["y"] + box["height"] / 2

        line = f"{label_index[ann.label_id]} {x_center} {y_center} {box['width']} {box['height']}"

        yolo.setdefault(item.data_url, []).append(line)

    return yolo
    import io
import zipfile
import json
import os

from fastapi.responses import StreamingResponse

@router.get("/{dataset_id}/zip")
async def export_zip(
    dataset_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    dataset = await session.get(Dataset, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

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

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:

        # -----------------
        # Labels
        # -----------------
        zipf.writestr(
            "labels.json",
            json.dumps(
                [{"id": l.id, "name": l.name, "color": l.color} for l in labels],
                indent=2,
            ),
        )

        # -----------------
        # Items + Annotations
        # -----------------
        for item in items:
            item_annotations = [
                a for a in annotations if a.item_id == item.id
            ]

            # Annotation JSON
            zipf.writestr(
                f"annotations/item_{item.id}.json",
                json.dumps(
                    {
                        "item_id": item.id,
                        "type": item.data_type,
                        "annotations": [
                            {
                                "label_id": a.label_id,
                                "value": a.value,
                            }
                            for a in item_annotations
                        ],
                    },
                    indent=2,
                ),
            )

            # Images (if image item)
            if item.data_type == "image":
                file_path = item.data_url.replace("/uploads/", "uploads/")
                if os.path.exists(file_path):
                    zipf.write(
                        file_path,
                        arcname=f"images/{os.path.basename(file_path)}",
                    )

    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={dataset.name}.zip"
        },
    )
