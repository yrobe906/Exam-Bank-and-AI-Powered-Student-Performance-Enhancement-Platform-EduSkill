# exam_models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base

class ExamModel(Base):  # Changed from 'Exam' to 'ExamModel'
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    sector_id = Column(Integer, ForeignKey("sectors.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(150), nullable=False)
    total_questions = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    total_marks = Column(Integer, nullable=False)
    exam_type = Column(String(50), nullable=False)
    # Pricing fields for Free/Premium feature
    pricing_type = Column(String(20), default="Free")  # "Free" or "Premium"
    amount = Column(Float, default=0)  # Amount in ETB for premium exams

    sector = relationship("SectorModel", back_populates="exams")
    sections = relationship("SectionModel", back_populates="exam", cascade="all, delete")
    unlock_requests = relationship("UnlockRequestModel", back_populates="exam")
    student_exam_unlocks = relationship("StudentExamUnlockModel", back_populates="exam")
