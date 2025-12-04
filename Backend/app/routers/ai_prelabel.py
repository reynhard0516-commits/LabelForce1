# app/routers/ai_prelabel.py
from fastapi import APIRouter, File, UploadFile, Depends
from app.workers.tasks import enqueue_prelabel
import tempfile, shutil, os
from app.database import SessionLocal

router = APIRouter()

@router.post("/prelabel")
def prelabel(file: UploadFile = File(...)):
    # save temporarily
    tmpd = tempfile.mkdtemp()
    path = os.path.join(tmpd, file.filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    job = enqueue_prelabel(path)
    return {"job_id": job.id, "status": "queued"}
