from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
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
    session: AsyncSession = Depends(get_session)
):
    # Fetch item
    result = await session.execute(
        select(DataItem).where(DataItem.id == item_id)
    )
    item = result.scalar_one_or_none()

    if not item or item.data_type != "text":
        raise HTTPException(status_code=404, detail="Text item not found")

    # Fetch labels
    labels = (await session.execute(
        select(Label).where(Label.dataset_id == item.dataset_id)
    )).scalars().all()

    if not labels:
        raise HTTPException(status_code=400, detail="No labels defined")

    label_names = [l.name for l in labels]

    # Call OpenAI
    prompt = f"""
    Text:
    {item.data_url}

    Choose the best label from:
    {", ".join(label_names)}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    predicted = response.choices[0].message.content.strip()

    label = next((l for l in labels if l.name.lower() == predicted.lower()), None)

    if not label:
        raise HTTPException(status_code=400, detail="AI label not matched")

    # Save annotation
    annotation = Annotation(
        item_id=item.id,
        label_id=label.id,
        user_id=None,  # AI-generated
        value="auto"
    )

    session.add(annotation)
    await session.commit()

    return {
        "item_id": item.id,
        "label": label.name,
        "confidence": "auto"
    }
