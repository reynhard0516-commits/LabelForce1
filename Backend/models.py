from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

# =====================================================
# DATASET
# =====================================================

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="datasets")
    items = relationship("DataItem", back_populates="dataset")


# =====================================================
# DATA ITEM (image / text / etc.)
# =====================================================

class DataItem(Base):
    __tablename__ = "data_items"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))

    data_type = Column(String)  # image, text, video, etc.
    data_url = Column(Text)     # file path or URL

    created_at = Column(DateTime, default=datetime.utcnow)

    dataset = relationship("Dataset", back_populates="items")
    annotations = relationship("Annotation", back_populates="item")


# =====================================================
# LABEL (class/category)
# =====================================================

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    color = Column(String)

    dataset_id = Column(Integer, ForeignKey("datasets.id"))


# =====================================================
# ANNOTATION (user label)
# =====================================================

class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("data_items.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    label_id = Column(Integer, ForeignKey("labels.id"))

    value = Column(Text)  # bounding box, text label, JSON, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    item = relationship("DataItem", back_populates="annotations")
datasets = relationship("Dataset", back_populates="owner")
