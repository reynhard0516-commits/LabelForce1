from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
    Boolean,
    JSON,
)
from sqlalchemy.orm import DeclarativeBase, relationship

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

    datasets = relationship("Dataset", back_populates="owner")
    annotations = relationship("Annotation", back_populates="user")


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
    items = relationship("DataItem", back_populates="dataset")
    labels = relationship("Label", back_populates="dataset")
    training_jobs = relationship("TrainingJob", back_populates="dataset")
    models = relationship("ModelArtifact", back_populates="dataset")


# =====================================================
# DATA ITEM
# =====================================================

class DataItem(Base):
    __tablename__ = "data_items"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)

    data_type = Column(String, nullable=False)   # text | image
    data_url = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    dataset = relationship("Dataset", back_populates="items")
    annotations = relationship("Annotation", back_populates="item")


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
    annotations = relationship("Annotation", back_populates="label")


# =====================================================
# ANNOTATION
# =====================================================

class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("data_items.id"), nullable=False)
    label_id = Column(Integer, ForeignKey("labels.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    value = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    item = relationship("DataItem", back_populates="annotations")
    label = relationship("Label", back_populates="annotations")
    user = relationship("User", back_populates="annotations")


# =====================================================
# TRAINING JOB (NEW)
# =====================================================

class TrainingJob(Base):
    __tablename__ = "training_jobs"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)

    task_type = Column(String, nullable=False)  # text | image
    status = Column(String, default="queued")  # queued | running | completed | failed

    metrics = Column(JSON)
    logs = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    dataset = relationship("Dataset", back_populates="training_jobs")


# =====================================================
# MODEL ARTIFACT (NEW)
# =====================================================

class ModelArtifact(Base):
    __tablename__ = "model_artifacts"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)

    task_type = Column(String, nullable=False)   # text | image
    version = Column(String, nullable=False)     # v1, v2, v3...
    path_or_url = Column(Text, nullable=False)

    is_active = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    dataset = relationship("Dataset", back_populates="models")
