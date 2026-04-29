from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    structure_id = Column(Integer, ForeignKey("exam_structures.id", ondelete="CASCADE"))
    question_text = Column(Text, nullable=False)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    correct_answer = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    explanation = Column(Text, nullable=True)
    pdf_file = Column(String, nullable=True)  # NEW: store uploaded PDF filename
    created_at = Column(DateTime, default=datetime.utcnow)
