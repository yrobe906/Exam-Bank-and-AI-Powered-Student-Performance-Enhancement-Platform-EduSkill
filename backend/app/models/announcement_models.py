from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from database import Base
from datetime import datetime


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)  # academic, achievement
    target_role = Column(String(50), nullable=False)  # student, teacher, both
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    file_path = Column(String(500))  # Path to uploaded PDF file
    file_name = Column(String(255))  # Original filename