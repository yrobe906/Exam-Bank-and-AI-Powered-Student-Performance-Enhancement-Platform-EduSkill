from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from .user_models import User
from .exam_models import ExamModel
from .section_models import SectionModel

class UnlockRequestModel(Base):
    __tablename__ = "unlock_requests"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id", ondelete="CASCADE"), nullable=True)
    content_id = Column(Integer, nullable=False)
    content_type = Column(String(50), nullable=False, default='mock_exam')
    exam_name = Column(String(200), nullable=False)
    unlock_method = Column(String(20), nullable=False)  # 'points' or 'payment'
    points_required = Column(Integer, nullable=False, default=0)
    price = Column(Float, nullable=False, default=0.0)
    payment_method = Column(String(20), nullable=True)  # 'cbe', 'boa', 'telebirr'
    payment_proof_path = Column(String(500), nullable=True)
    status = Column(String(20), default="pending", index=True)  # pending, approved, rejected
    payment_verified = Column(Boolean, default=False)
    pricing_type = Column(String(20), nullable=True)
    transaction_ref = Column(String(100), nullable=True)
    admin_notes = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="unlock_requests")
    exam = relationship("ExamModel")
    section = relationship("SectionModel")

class StudentExamUnlockModel(Base):
    __tablename__ = "student_exam_unlocks"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="CASCADE"), nullable=False, index=True)
    section_id = Column(Integer, ForeignKey("sections.id", ondelete="CASCADE"), nullable=True, index=True)
    unlock_method = Column(String(20), nullable=False, default='request')
    points_used = Column(Integer, default=0)
    pricing_type = Column(String(20), nullable=True)
    payment_proof = Column(String(500), nullable=True)
    unlocked_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="student_exam_unlocks")
    exam = relationship("ExamModel")
    section = relationship("SectionModel")

# Add back_populates to existing models (will update later)
# User.unlock_requests = relationship("UnlockRequestModel", back_populates="user", cascade="all, delete-orphan")
# User.student_exam_unlocks = relationship("StudentExamUnlockModel", back_populates="user")
# ExamModel.unlock_requests = relationship("UnlockRequestModel", back_populates="exam")
# ExamModel.student_exam_unlocks = relationship("StudentExamUnlockModel", back_populates="exam")
