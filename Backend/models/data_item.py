from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class DataItem(Base):
    __tablename__ = "data_items"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    data_type = Column(String)
    data_url = Column(String)

    dataset = relationship("Dataset", back_populates="items")
    annotations = relationship("Annotation", back_populates="item")
