from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class StudentAnswerModel(Base):
    __tablename__ = "student_answers"
    __table_args__ = {"extend_existing": True}  # Prevent "table already defined" errors

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    attempt_id = Column(Integer, ForeignKey("exam_attempts.id", ondelete="CASCADE"), nullable=False)
    # The actual DB table is named `question` (singular) — match the existing schema
    question_id = Column(Integer, ForeignKey("question.id", ondelete="CASCADE"), nullable=False)

    # Student's selected answer
    selected_answer = Column(String(1), nullable=False)  # A, B, C, D
    is_correct = Column(Boolean, default=False)

    # Relationships
    attempt = relationship(
        "ExamAttemptModel",
        back_populates="student_answers"
    )

    question = relationship(
        "QuestionModel"  # Make sure your question model class is named QuestionModel
    )
