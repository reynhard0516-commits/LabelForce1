from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text
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
    role = Column(String, default="user")  # user | admin

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

    # Relationships
    owner = relationship("User", back_populates="datasets")
    items = relationship(
        "DataItem",
        back_populates="dataset",
        cascade="all, delete-orphan"
    )
    labels = relationship(
        "Label",
        back_populates="dataset",
        cascade="all, delete-orphan"
    )


# =====================================================
# DATA ITEM (image / text / video / etc.)
# =====================================================

class DataItem(Base):
    __tablename__ = "data_items"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)

    data_type = Column(String, nullable=False)   # image, text, video
    data_url = Column(Text, nullable=False)      # path or URL

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    dataset = relationship("Dataset", back_populates="items")
    annotations = relationship(
        "Annotation",
        back_populates="item",
        cascade="all, delete-orphan"
    )


# =====================================================
# LABEL (class / category)
# =====================================================

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    color = Column(String)

    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)

    # Relationships
    dataset = relationship("Dataset", back_populates="labels")
    annotations = relationship(
        "Annotation",
        back_populates="label",
        cascade="all, delete-orphan"
    )


# =====================================================
# ANNOTATION (user-generated label)
# =====================================================

class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("data_items.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    label_id = Column(Integer, ForeignKey("labels.id"), nullable=False)

    value = Column(Text)  # bbox, polygon, text, JSON
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    item = relationship("DataItem", back_populates="annotations")
    user = relationship("User", back_populates="annotations")
    label = relationship("Label", back_populates="annotations")
