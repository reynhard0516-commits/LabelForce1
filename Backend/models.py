from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship, DeclarativeBase

# =====================================================
# BASE
# =====================================================

class Base(DeclarativeBase):
    pass

# =====================================================
# USER
# =====================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    datasets = relationship("Dataset", back_populates="owner", cascade="all, delete")
    annotations = relationship("Annotation", back_populates="user", cascade="all, delete")

# =====================================================
# DATASET
# =====================================================

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="datasets")
    items = relationship("DataItem", back_populates="dataset", cascade="all, delete")
    labels = relationship("Label", back_populates="dataset", cascade="all, delete")

# =====================================================
# DATA ITEM (text / image / video)
# =====================================================

class DataItem(Base):
    __tablename__ = "data_items"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)

    data_type = Column(String, nullable=False)  # text, image, video
    data_url = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    dataset = relationship("Dataset", back_populates="items")
    annotations = relationship("Annotation", back_populates="item", cascade="all, delete")

# =====================================================
# LABEL
# =====================================================

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    color = Column(String)

    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)

    dataset = relationship("Dataset", back_populates="labels")
    annotations = relationship("Annotation", back_populates="label", cascade="all, delete")

# =====================================================
# ANNOTATION
# =====================================================

class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True)

    item_id = Column(Integer, ForeignKey("data_items.id"), nullable=False)
    label_id = Column(Integer, ForeignKey("labels.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    value = Column(JSON)  # bbox, polygon, text, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    item = relationship("DataItem", back_populates="annotations")
    label = relationship("Label", back_populates="annotations")
    user = relationship("User", back_populates="annotations")
