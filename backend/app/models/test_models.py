from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

class TestModel(Base):  # Make sure this is TestModel, not Test
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    sector_id = Column(Integer, ForeignKey("sectors.id", ondelete="SET NULL"))
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="SET NULL"))
    duration = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    question_count = Column(Integer, nullable=False)
    created_by = Column(Integer, nullable=False)
    is_draft = Column(Boolean, default=True)