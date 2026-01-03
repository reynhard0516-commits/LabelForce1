from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True)
    data_item_id = Column(Integer, ForeignKey("data_items.id"))
    label_id = Column(Integer, ForeignKey("labels.id"))
    data = Column(JSON)  # bbox, text span, etc.

    item = relationship("DataItem", back_populates="annotations")
    label = relationship("Label", back_populates="annotations")
