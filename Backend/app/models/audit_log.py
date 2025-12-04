
from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True)
    action = Column(String)
    entity = Column(String)
    details = Column(String)
    user_id = Column(Integer)
    timestamp = Column(DateTime, server_default=func.now())
