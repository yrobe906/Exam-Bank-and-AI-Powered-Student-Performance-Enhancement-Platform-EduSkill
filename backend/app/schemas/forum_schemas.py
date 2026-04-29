from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Schema for creating a forum post
class ForumPostCreate(BaseModel):
    title: str
    content: str
    category: str  # Q&A, Study Tips, Exam Advice, Motivation, Stress, General

# Schema for forum post response
class ForumPostResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    user_id: int
    username: str
    user_role: str
    profile_image: Optional[str] = None
    is_pinned: bool
    is_approved: bool
    created_at: datetime
    updated_at: datetime
    likes_count: int = 0
    comments_count: int = 0
    is_liked: bool = False
    is_bookmarked: bool = False

    class Config:
        from_attributes = True

# Schema for creating a comment
class ForumCommentCreate(BaseModel):
    content: str

# Schema for comment response
class ForumCommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    username: str
    user_role: str
    profile_image: Optional[str] = None
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

# Schema for like/unlike
class ForumLikeRequest(BaseModel):
    post_id: int

# Schema for bookmark/unbookmark
class ForumBookmarkRequest(BaseModel):
    post_id: int

# Schema for pinning a post (teacher only)
class ForumPinRequest(BaseModel):
    post_id: int
    is_pinned: bool
