# analytics_schemas.py
# Pydantic schemas for Analytics API responses
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# ==================== Subject Analytics ====================

class SubjectAnalyticsBase(BaseModel):
    """Base schema for subject analytics"""
    sector_id: int
    sector_name: str
    total_exams_taken: int
    average_score: float
    highest_score: int
    lowest_score: int
    total_questions_attempted: int
    total_correct_answers: int
    accuracy_percentage: float


class SubjectAnalyticsResponse(SubjectAnalyticsBase):
    """Response schema for subject analytics"""
    id: int
    calculated_at: datetime

    class Config:
        from_attributes = True


# ==================== Topic Analytics ====================

class TopicAnalyticsBase(BaseModel):
    """Base schema for topic analytics"""
    section_id: int
    section_name: str
    sector_id: int
    sector_name: str
    total_exams_taken: int
    average_score: float
    total_questions_attempted: int
    total_correct_answers: int
    accuracy_percentage: float
    recent_scores: List[float] = []
    is_weak_topic: bool
    weakness_level: int  # 0=None, 1=Mild, 2=Moderate, 3=Severe


class TopicAnalyticsResponse(TopicAnalyticsBase):
    """Response schema for topic analytics"""
    id: int
    calculated_at: datetime

    class Config:
        from_attributes = True


# ==================== Overall Summary ====================

class OverallSummaryResponse(BaseModel):
    """Response schema for overall student summary"""
    student_id: int
    total_exams_taken: int
    average_score: float
    highest_score: int
    lowest_score: int
    total_study_time_minutes: int
    total_subjects_studied: int
    total_topics_covered: int
    weak_topics_count: int
    class_rank: Optional[int] = None
    calculated_at: datetime

    class Config:
        from_attributes = True


# ==================== Progress Analytics ====================

class ProgressEntry(BaseModel):
    """Single progress entry for charts"""
    date: str
    exams_taken: int
    score: float
    questions_attempted: int
    correct_answers: int
    accuracy: float
    study_time_minutes: int


class ProgressHistoryResponse(BaseModel):
    """Response schema for progress history"""
    student_id: int
    progress_data: List[ProgressEntry]
    total_entries: int

    class Config:
        from_attributes = True


# ==================== Weak Topics ====================

class WeakTopicResponse(BaseModel):
    """Response schema for weak topics"""
    section_id: int
    section_name: str
    sector_id: int
    sector_name: str
    average_score: float
    recent_scores: List[float]
    weakness_level: int  # 1=Mild, 2=Moderate, 3=Severe
    exam_count: int
    trend: str  # "improving", "declining", "stagnant"
    recommendation: str

    class Config:
        from_attributes = True


class WeakTopicsListResponse(BaseModel):
    """Response schema for list of weak topics"""
    student_id: int
    weak_topics: List[WeakTopicResponse]
    total_weak_topics: int

    class Config:
        from_attributes = True


# ==================== AI Recommendations ====================

class AIRecommendationBase(BaseModel):
    """Base schema for AI recommendations"""
    recommendation_type: str  # 'weak_topic', 'improving', 'practice', 'advance'
    priority: int  # 1=High, 2=Medium, 3=Low
    title: str
    description: Optional[str] = None
    sector_id: Optional[int] = None
    section_id: Optional[int] = None
    sector_name: Optional[str] = None


class AIRecommendationResponse(AIRecommendationBase):
    """Response schema for AI recommendations"""
    id: int
    is_read: bool
    is_actioned: bool
    created_at: datetime
    trigger_data: Dict[str, Any] = {}

    class Config:
        from_attributes = True


class RecommendationsListResponse(BaseModel):
    """Response schema for list of recommendations"""
    student_id: int
    recommendations: List[AIRecommendationResponse]
    total_recommendations: int
    high_priority_count: int

    class Config:
        from_attributes = True


# ==================== Dashboard Summary ====================

class QuickStat(BaseModel):
    """Quick stat for dashboard"""
    label: str
    value: str
    change: Optional[str] = None
    change_type: Optional[str] = None  # "positive", "negative", "neutral"


class FlashcardStats(BaseModel):
    """Flashcard statistics for dashboard"""
    total_cards_reviewed: int = 0
    learning_count: int = 0
    known_count: int = 0
    revisit_count: int = 0
    total_reviews: int = 0
    mastery_percentage: float = 0.0


class PracticeMockStats(BaseModel):
    """Practice mock test statistics for dashboard"""
    total_tests_taken: int = 0
    average_score: float = 0.0
    highest_score: float = 0.0
    lowest_score: float = 0.0
    total_questions_attempted: int = 0
    total_correct: int = 0
    subjects_practiced: List[str] = []


class DashboardSummaryResponse(BaseModel):
    """Complete dashboard summary for a student"""
    student_id: int
    # Quick stats
    average_score: float
    total_exams_taken: int
    weak_topics_count: int
    class_rank: Optional[int] = None
    # Change from last period
    score_change: float = 0.0
    exams_change: int = 0
    # Subject breakdown
    subjects: List[SubjectAnalyticsBase]
    # Top performers
    strongest_topic: Optional[TopicAnalyticsBase] = None
    weakest_topic: Optional[TopicAnalyticsBase] = None
    # Recent recommendations
    recent_recommendations: List[AIRecommendationBase] = []
    # Progress data (last 7 days)
    weekly_progress: List[ProgressEntry] = []
    # Flashcard stats
    flashcard_stats: Optional[FlashcardStats] = None
    # Practice mock test stats
    practice_mock_stats: Optional[PracticeMockStats] = None

    class Config:
        from_attributes = True


# ==================== Calculate Request ====================

class CalculateAnalyticsRequest(BaseModel):
    """Request to trigger analytics calculation"""
    student_id: Optional[int] = None  # Optional since it's provided in URL path
    force_refresh: bool = False  # Force recalculation even if recent data exists


class CalculateAnalyticsResponse(BaseModel):
    """Response after triggering analytics calculation"""
    student_id: int
    success: bool
    message: str
    calculated_subjects: int
    calculated_topics: int
    recommendations_generated: int
    calculated_at: datetime

    class Config:
        from_attributes = True
