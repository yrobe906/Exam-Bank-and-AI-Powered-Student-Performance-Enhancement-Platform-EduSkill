# section_models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class SectionModel(Base):  # Changed from 'Section' to 'SectionModel'
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(150), nullable=False)
    question_count = Column(Integer, nullable=False)
    color = Column(String(50), nullable=True)

    exam = relationship("ExamModel", back_populates="sections")
    questions = relationship("QuestionModel", back_populates="section", cascade="all, delete")
    # Relationships for section feedback
    ratings = relationship("SectionRating", back_populates="section", cascade="all, delete")
    feedbacks = relationship("SectionFeedback", back_populates="section", cascade="all, delete")
