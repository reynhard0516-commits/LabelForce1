# app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.task import Task
from app.models.taskunit import TaskUnit
from typing import List
import io

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_task(project_id: int, title: str = "", db: Session = Depends(get_db)):
    t = Task(project_id=project_id, file_path="", label="", status="unlabeled")
    db.add(t); db.commit(); db.refresh(t)
    return {"ok": True, "id": t.id}

@router.post("/{task_id}/upload_units")
def upload_units(task_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Accepts newline-separated payloads (image URLs or identifiers) and creates TaskUnits.
    """
    data = file.file.read().decode("utf-8").strip().splitlines()
    created = 0
    for line in data:
        tu = TaskUnit(task_id=task_id, payload=line.strip(), status="unassigned", reward=0.2)
        db.add(tu); created += 1
    db.commit()
    return {"ok": True, "created": created}

@router.get("/available", response_model=List[dict])
def available(limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(TaskUnit).filter_by(status="unassigned").limit(limit).all()
    return [{"id": i.id, "payload": i.payload, "reward": i.reward} for i in items]

@router.post("/claim/{unit_id}")
def claim(unit_id: int, worker_id: int, db: Session = Depends(get_db)):
    unit = db.query(TaskUnit).get(unit_id)
    if not unit or unit.status != "unassigned":
        raise HTTPException(404, "Not available")
    unit.status = "assigned"; unit.assigned_to = worker_id
    db.add(unit); db.commit(); db.refresh(unit)
    return {"ok": True, "unit_id": unit.id}

@router.post("/submit/{unit_id}")
def submit(unit_id: int, result: dict, worker_id: int, db: Session = Depends(get_db)):
    unit = db.query(TaskUnit).get(unit_id)
    if not unit or unit.assigned_to != worker_id:
        raise HTTPException(403, "Not assigned to you")
    unit.submitted_result = str(result); unit.status = "submitted"
    db.add(unit)
    # credit logic would run here (payments module)
    db.commit(); db.refresh(unit)
    return {"ok": True}
