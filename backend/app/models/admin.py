from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.sql import func
from database import Base

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=True)  # Changed to nullable=True
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="admin")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AdminUnlockRequest(Base):
    __tablename__ = "admin_unlock_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    user_xp = Column(Integer, default=0)
    user_tier = Column(String, default="bronze")
    user_streak = Column(Integer, default=0)
    content_type = Column(String, nullable=False)  # 'exam', 'resource', etc.
    content_id = Column(Integer, nullable=False)
    content_title = Column(String, nullable=False)
    unlock_method = Column(String, nullable=False)  # 'payment', 'points'
    points_used = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    payment_method = Column(String, nullable=True)
    transaction_ref = Column(String, nullable=True)
    request_reason = Column(Text, nullable=True)
    status = Column(String, default="pending")  # 'pending', 'approved', 'rejected'
    payment_proof_path = Column(String, nullable=True)
    admin_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    processed_by = Column(Integer, nullable=True)  # admin_id


class UserPremiumAccess(Base):
    __tablename__ = "user_premium_access"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    content_type = Column(String, nullable=False)  # 'exam', 'resource', etc.
    content_id = Column(Integer, nullable=False)
    access_granted_at = Column(DateTime(timezone=True), server_default=func.now())
    granted_by = Column(Integer, nullable=True)  # admin_id who granted access
    payment_method = Column(String, nullable=True)  # 'direct_payment', 'admin_approval'