# sector_models.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base

class SectorModel(Base):  # Changed from 'Sector' to 'SectorModel'
    __tablename__ = "sectors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    icon = Column(String(255), nullable=True)

    exams = relationship("ExamModel", back_populates="sector", cascade="all, delete")