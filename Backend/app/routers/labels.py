# app/routers/labels.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.label import Label
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LabelCreate(BaseModel):
    sku: str
    product_name: Optional[str] = None
    group_name: Optional[str] = None

@router.post("/", response_model=dict)
def create_label(payload: LabelCreate, db: Session = Depends(get_db)):
    exists = db.query(Label).filter_by(sku=payload.sku).first()
    if exists:
        raise HTTPException(400, "SKU already exists")
    l = Label(sku=payload.sku, product_name=payload.product_name or "", group_name=payload.group_name)
    db.add(l); db.commit(); db.refresh(l)
    return {"ok": True, "id": l.id}

@router.get("/", response_model=List[dict])
def list_labels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(Label).offset(skip).limit(limit).all()
    return [{"id": i.id, "sku": i.sku, "product_name": i.product_name, "group": i.group_name} for i in items]

@router.get("/{sku}")
def get_by_sku(sku: str, db: Session = Depends(get_db)):
    item = db.query(Label).filter_by(sku=sku).first()
    if not item:
        raise HTTPException(404, "Not found")
    return {"id": item.id, "sku": item.sku, "product_name": item.product_name, "group": item.group_name}

@router.delete("/{sku}")
def delete_label(sku: str, db: Session = Depends(get_db)):
    item = db.query(Label).filter_by(sku=sku).first()
    if not item:
        raise HTTPException(404, "Not found")
    db.delete(item); db.commit()
    return {"ok": True}
