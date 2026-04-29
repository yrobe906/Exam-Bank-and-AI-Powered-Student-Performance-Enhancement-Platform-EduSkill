from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    subject = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    access_type = Column(String(20), default="free")  # "free" or "premium"
    price = Column(Float, default=0.0)
    theme_color = Column(String(50), default="blue")
    font_style = Column(String(50), default="sans-serif")
    uploaded_by = Column(Integer, nullable=True)  # Teacher who uploaded the note
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
