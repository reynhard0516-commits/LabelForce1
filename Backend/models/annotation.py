from sqlalchemy import Column, Integer, ForeignKey, String
from database import Base

class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True)
    data_item_id = Column(Integer, ForeignKey("data_items.id"))
    label_id = Column(Integer, ForeignKey("labels.id"))
    value = Column(String)
