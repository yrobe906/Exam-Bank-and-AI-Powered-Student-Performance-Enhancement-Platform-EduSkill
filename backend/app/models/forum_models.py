from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class ForumPost(Base):
    __tablename__ = "forum_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)  # Q&A, Study Tips, Exam Advice, Motivation, Stress, General
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    username = Column(String(100), nullable=False)
    user_role = Column(String(20), nullable=False)  # student, teacher
    profile_image = Column(String(500), nullable=True)
    is_pinned = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="forum_posts")
    likes = relationship("ForumPostLike", back_populates="post", cascade="all, delete-orphan")
    comments = relationship("ForumComment", back_populates="post", cascade="all, delete-orphan")

class ForumPostLike(Base):
    __tablename__ = "forum_post_likes"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("forum_posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    post = relationship("ForumPost", back_populates="likes")

class ForumComment(Base):
    __tablename__ = "forum_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("forum_posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    username = Column(String(100), nullable=False)
    user_role = Column(String(20), nullable=False)
    profile_image = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    post = relationship("ForumPost", back_populates="comments")

class ForumBookmark(Base):
    __tablename__ = "forum_bookmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("forum_posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    post = relationship("ForumPost")
