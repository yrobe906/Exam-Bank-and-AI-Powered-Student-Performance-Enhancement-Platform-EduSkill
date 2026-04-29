from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class ExamStructure(Base):
    __tablename__ = "exam_structures"

    id = Column(Integer, primary_key=True, index=True)
    exam_type = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
    university = Column(String, nullable=True)
    model_type = Column(String, nullable=True)
    subject = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
