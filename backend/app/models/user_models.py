from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
from .gamification_models import GamificationActivityModel
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=False)

    # Student fields
    school_id = Column(String(100))
    grade = Column(Integer)

    # Teacher fields
    phone = Column(String(20))
    school_name = Column(String(255))
    subject_assigned = Column(String(100))
    teaching_grade = Column(Integer)

    # EduOffice fields
    woreda = Column(String(100))
    school_supervising = Column(String(255))

    profile_photo = Column(String(255))
    status = Column(String(50), default="pending")
    xp_points = Column(Integer, default=0)
    current_tier = Column(String(20), default="bronze")
    created_at = Column(DateTime, default=datetime.utcnow)

# Relationships
    forum_posts = relationship("ForumPost", back_populates="user")
    
    gamification_activities = relationship("GamificationActivityModel", back_populates="user")

    # Relationships for unlock features
    unlock_requests = relationship("UnlockRequestModel", back_populates="user", cascade="all, delete-orphan")
    student_exam_unlocks = relationship("StudentExamUnlockModel", back_populates="user", cascade="all, delete-orphan")

    # Relationships for section feedback
    section_ratings = relationship("SectionRating", back_populates="user")

    # Password reset tokens
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user", cascade="all, delete-orphan")
    section_feedback = relationship("SectionFeedback", back_populates="user")

