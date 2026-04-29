from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class PracticeMockTest(Base):
    __tablename__ = "practice_mock_tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, default=30)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PracticeQuestion(Base):
    __tablename__ = "practice_questions"

    id = Column(Integer, primary_key=True, index=True)
    mock_test_id = Column(Integer, ForeignKey("practice_mock_tests.id", ondelete="CASCADE"), nullable=False)
    question_text = Column(Text, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)  # a, b, c, or d
    explanation = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class PracticeMockAttempt(Base):
    """
    Tracks student practice mock test attempts and results.
    """
    __tablename__ = "practice_mock_attempts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mock_test_id = Column(Integer, ForeignKey("practice_mock_tests.id"), nullable=False)
    
    # Score information
    score = Column(Integer, default=0)  # Number of correct answers
    total_questions = Column(Integer, default=0)
    percentage = Column(Float, default=0.0)  # Percentage score
    
    # Time tracking
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    time_taken_seconds = Column(Integer, default=0)
    
    # Status
    is_completed = Column(Boolean, default=False)
    
    # Relationship
    mock_test = relationship("PracticeMockTest")
