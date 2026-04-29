from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# -----------------------------
# Exam Attempt Model ONLY
# -----------------------------
class ExamAttemptModel(Base):
    __tablename__ = "exam_attempts"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)

    score = Column(Integer, default=0)

    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationship to student answers (reference the model from other file)
    student_answers = relationship(
        "StudentAnswerModel",  # This will be imported from student_answer_models.py
        back_populates="attempt",
        cascade="all, delete"
    )