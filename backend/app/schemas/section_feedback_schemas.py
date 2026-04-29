# section_feedback_schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ==================== RATING SCHEMAS ====================

class SectionRatingBase(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")


class SectionRatingCreate(SectionRatingBase):
    section_id: int


class SectionRatingUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)


class SectionRatingResponse(SectionRatingBase):
    id: int
    section_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== FEEDBACK SCHEMAS ====================

class SectionFeedbackBase(BaseModel):
    feedback_text: str = Field(..., min_length=1, max_length=500)
    is_anonymous: bool = True


class SectionFeedbackCreate(SectionFeedbackBase):
    section_id: int


class SectionFeedbackUpdate(BaseModel):
    feedback_text: Optional[str] = Field(None, min_length=1, max_length=500)
    is_anonymous: Optional[bool] = None


class SectionFeedbackResponse(SectionFeedbackBase):
    id: int
    section_id: int
    user_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== SECTION WITH RATINGS ====================

class SectionWithRatings(BaseModel):
    """Section information with rating data"""
    section_id: int
    section_name: str
    exam_title: str
    sector_name: str
    sector_icon: Optional[str] = None
    question_count: int
    grade_level: int
    average_rating: float = 0.0
    total_ratings: int = 0
    user_rating: Optional[int] = None

    class Config:
        from_attributes = True


# ==================== FEEDBACK STATS ====================

class FeedbackStats(BaseModel):
    """Feedback statistics for admin/teachers"""
    total_feedbacks: int
    today_feedbacks: int
    anonymous_count: int
    recent_feedbacks: List[SectionFeedbackResponse] = []


class SectionFeedbackWithSection(SectionFeedbackResponse):
    """Feedback with section details (for admin view)"""
    section_name: Optional[str] = None
    exam_title: Optional[str] = None


# ==================== SUBMIT FEEDBACK REQUEST ====================

class SubmitFeedbackRequest(BaseModel):
    # section_id is in the URL path, not needed in request body
    rating: Optional[int] = Field(None, ge=1, le=5, description="Optional rating 1-5")
    feedback_text: Optional[str] = Field(None, max_length=500, description="Optional feedback text")
    is_anonymous: bool = True


class SubmitFeedbackResponse(BaseModel):
    success: bool
    message: str
    rating_submitted: bool = False
    feedback_submitted: bool = False


# ==================== FEEDBACK MODERATION SCHEMAS ====================

class FeedbackModerateRequest(BaseModel):
    """Request schema for moderating feedback"""
    rating: Optional[int] = Field(None, ge=1, le=5, description="Updated rating 1-5")
    feedback_text: Optional[str] = Field(None, min_length=1, max_length=500, description="Updated feedback text")
    status: Optional[str] = Field(None, description="Status: 'pending' or 'reviewed'")
    internal_notes: Optional[str] = Field(None, max_length=1000, description="Internal notes for admin/edu_office")


class FeedbackModerateResponse(BaseModel):
    """Response schema for moderated feedback"""
    id: int
    section_id: int
    user_id: Optional[int]
    feedback_text: str
    is_anonymous: bool
    rating: Optional[int] = None
    status: str
    internal_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    student_name: Optional[str] = None
    username: Optional[str] = None
    grade_level: Optional[int] = None
    section_name: Optional[str] = None

    class Config:
        from_attributes = True


# ==================== FEEDBACK LIST RESPONSE ====================

class FeedbackListResponse(BaseModel):
    """Response schema for feedback list with stats"""
    feedback: List[FeedbackModerateResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
    stats: Optional[dict] = None


# ==================== EXPORT REQUEST SCHEMA ====================

class ExportFeedbackRequest(BaseModel):
    """Request parameters for exporting feedback"""
    format: str = Field(..., description="Export format: 'pdf' or 'excel'")
    grade: Optional[int] = Field(None, description="Filter by grade level")
    section: Optional[str] = Field(None, description="Filter by section name")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Filter by rating")
    start_date: Optional[str] = Field(None, description="Start date filter (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date filter (YYYY-MM-DD)")
    include_anonymous: bool = Field(True, description="Include anonymous feedback")
    section_id: Optional[int] = Field(None, description="Filter by section ID")

