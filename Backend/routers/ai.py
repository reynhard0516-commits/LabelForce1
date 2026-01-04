from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import DataItem, Label, Annotation
from auth import decode_token

import os
import openai

router = APIRouter(
    prefix="/ai",
    tags=["ai"]
)

openai.api_key = os.getenv("OPENAI_API_KEY")


@router.post("/auto-label/{item_id}")
async def auto_label_text(
    item_id: int,
    token=Depends(decode_token),
    db: AsyncSession = Depends(get_db),
):
    # -----------------------------
    # Fetch item
    # -----------------------------
    result = await db.execute(
        select(DataItem).where(DataItem.id == item_id)
    )
    item = result.scalar_one_or_none()

    if not item or item.data_type != "text":
        raise HTTPException(status_code=404, detail="Text item not found")

    # -----------------------------
    # Fetch labels
    # -----------------------------
    labels = (
        await db.execute(
            select(Label).where(Label.dataset_id == item.dataset_id)
        )
    ).scalars().all()

    if not labels:
        raise HTTPException(status_code=400, detail="No labels defined")

    label_names = [l.name for l in labels]

    # -----------------------------
    # OpenAI prompt
    # -----------------------------
    prompt = f"""
Text:
{item.data_url}

Choose the best label from:
{", ".join(label_names)}

Return ONLY the label name.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    predicted = response.choices[0].message.content.strip()

    label = next(
        (l for l in labels if l.name.lower() == predicted.lower()),
        None
    )

    if not label:
        raise HTTPException(
            status_code=400,
            detail=f"AI label '{predicted}' not matched"
        )

    # -----------------------------
    # Save annotation
    # -----------------------------
    annotation = Annotation(
        item_id=item.id,
        label_id=label.id,
        user_id=None,      # AI-generated
        value="auto"
    )

    db.add(annotation)
    await db.commit()

    return {
        "item_id": item.id,
        "label": label.name,
        "source": "ai"
    }
