from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base



class GamificationActivityModel(Base):
    __tablename__ = 'gamification_activities'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    activity_type = Column(String(50), nullable=False)  # 'exam_submission', 'exam_result', etc.
    content_id = Column(Integer)  # exam_id, etc.
    content_type = Column(String(50))  # 'exam'
    xp_awarded = Column(Integer, default=0)
    is_cooldown_active = Column(Boolean, default=False)
    cooldown_until = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship('User', back_populates='gamification_activities')
