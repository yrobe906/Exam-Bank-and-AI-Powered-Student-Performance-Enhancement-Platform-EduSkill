from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Resource(Base):
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    type = Column(String(20), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(200), nullable=False)
    file_size = Column(Integer)
    subject = Column(String(100), nullable=False)
    grade_level = Column(String(20), nullable=False)
    is_premium = Column(Boolean, default=False)
    price = Column(Float, default=0.0)
    preview_path = Column(String(500), nullable=True)
    uploaded_by = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
