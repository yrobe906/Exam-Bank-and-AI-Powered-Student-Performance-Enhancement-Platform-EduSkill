# section_feedback_models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class SectionRating(Base):
    """Model for section ratings by students"""
    __tablename__ = "section_ratings"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("sections.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    section = relationship("SectionModel", back_populates="ratings")
    user = relationship("User", back_populates="section_ratings")


class SectionFeedback(Base):
    """Model for anonymous feedback about sections"""
    __tablename__ = "section_feedback"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("sections.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)  # Can be null for anonymous
    feedback_text = Column(Text, nullable=False)
    is_anonymous = Column(Boolean, default=True)
    rating = Column(Integer, nullable=True)  # 1-5 stars (optional, linked to feedback)
    status = Column(String(20), default="pending")  # 'pending' or 'reviewed'
    internal_notes = Column(Text, nullable=True)  # Internal notes for admin/edu_office
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    section = relationship("SectionModel", back_populates="feedbacks")
    user = relationship("User", back_populates="section_feedback")



