from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from database import get_session
from models import Dataset, TrainingJob, ModelArtifact
from auth import decode_token

router = APIRouter(
    prefix="/training",
    tags=["training"]
)

# =====================================================
# START TRAINING
# =====================================================

@router.post("/start/{dataset_id}")
async def start_training(
    dataset_id: int,
    task_type: str = "text",  # text | image
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session),
):
    # Ensure dataset exists
    dataset = (
        await session.execute(
            select(Dataset).where(Dataset.id == dataset_id)
        )
    ).scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    job = TrainingJob(
        dataset_id=dataset_id,
        task_type=task_type,
        status="queued",
    )

    session.add(job)
    await session.commit()
    await session.refresh(job)

    return {
        "job_id": job.id,
        "status": job.status,
        "message": "Training job queued",
    }


# =====================================================
# GET TRAINING STATUS
# =====================================================

@router.get("/status/{job_id}")
async def get_training_status(
    job_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session),
):
    job = await session.get(TrainingJob, job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Training job not found")

    return {
        "job_id": job.id,
        "dataset_id": job.dataset_id,
        "task_type": job.task_type,
        "status": job.status,
        "metrics": job.metrics,
        "created_at": job.created_at,
        "completed_at": job.completed_at,
    }


# =====================================================
# LIST TRAINING HISTORY
# =====================================================

@router.get("/history/{dataset_id}")
async def training_history(
    dataset_id: int,
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session),
):
    jobs = (
        await session.execute(
            select(TrainingJob)
            .where(TrainingJob.dataset_id == dataset_id)
            .order_by(TrainingJob.created_at.desc())
        )
    ).scalars().all()

    return [
        {
            "id": j.id,
            "task_type": j.task_type,
            "status": j.status,
            "created_at": j.created_at,
            "completed_at": j.completed_at,
        }
        for j in jobs
    ]


# =====================================================
# MARK TRAINING COMPLETE (INTERNAL / FUTURE WORKER)
# =====================================================

@router.post("/complete/{job_id}")
async def complete_training(
    job_id: int,
    metrics: dict | None = None,
    model_path: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    job = await session.get(TrainingJob, job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Training job not found")

    job.status = "completed"
    job.completed_at = datetime.utcnow()
    job.metrics = metrics or {}

    # Save model artifact
    if model_path:
        model = ModelArtifact(
            dataset_id=job.dataset_id,
            task_type=job.task_type,
            version=f"v{job.id}",
            path_or_url=model_path,
            is_active=True,
        )
        session.add(model)

    await session.commit()

    return {
        "job_id": job.id,
        "status": "completed",
    }
