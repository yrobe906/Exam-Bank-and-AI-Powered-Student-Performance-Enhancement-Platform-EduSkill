# analytics_models.py
# Pre-calculated analytics tables for better performance
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON, Text

from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class StudentSubjectAnalytics(Base):
    """
    Stores pre-calculated subject-wise performance for each student.
    This table stores aggregated analytics data for faster queries.
    """
    __tablename__ = "student_subject_analytics"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    sector_id = Column(Integer, ForeignKey("sectors.id"), nullable=False, index=True)
    
    # Subject/sector name (cached for quick access)
    sector_name = Column(String(150), nullable=False)
    
    # Aggregated scores
    total_exams_taken = Column(Integer, default=0)
    average_score = Column(Float, default=0.0)
    highest_score = Column(Integer, default=0)
    lowest_score = Column(Integer, default=0)
    total_questions_attempted = Column(Integer, default=0)
    total_correct_answers = Column(Integer, default=0)
    
    # Calculated at
    calculated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sector = relationship("SectorModel")


class StudentTopicAnalytics(Base):
    """
    Stores pre-calculated topic-wise performance for each student.
    Topics refer to sections within exams.
    """
    __tablename__ = "student_topic_analytics"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    sector_id = Column(Integer, ForeignKey("sectors.id"), nullable=False, index=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False, index=True)
    
    # Topic info (cached for quick access)
    sector_name = Column(String(150), nullable=False)
    section_name = Column(String(150), nullable=False)
    
    # Aggregated scores
    total_exams_taken = Column(Integer, default=0)
    average_score = Column(Float, default=0.0)
    total_questions_attempted = Column(Integer, default=0)
    total_correct_answers = Column(Integer, default=0)
    
    # Recent exam scores (last 5) for trend analysis - stored as JSON
    recent_scores = Column(JSON, default=list)
    
    # AI Analysis flags
    is_weak_topic = Column(Integer, default=0)  # 0=No, 1=Yes
    weakness_level = Column(Integer, default=0)  # 0=None, 1=Mild, 2=Moderate, 3=Severe
    
    # Calculated at
    calculated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    section = relationship("SectionModel")


class StudentOverallAnalytics(Base):
    """
    Stores overall performance summary for each student.
    """
    __tablename__ = "student_overall_analytics"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    
    # Overall stats
    total_exams_taken = Column(Integer, default=0)
    average_score = Column(Float, default=0.0)
    highest_score = Column(Integer, default=0)
    lowest_score = Column(Integer, default=0)
    total_study_time_minutes = Column(Integer, default=0)
    
    # Performance metrics
    total_subjects_studied = Column(Integer, default=0)
    total_topics_covered = Column(Integer, default=0)
    weak_topics_count = Column(Integer, default=0)
    
    # Rank (if available)
    class_rank = Column(Integer, nullable=True)
    
    # Calculated at
    calculated_at = Column(DateTime, default=datetime.utcnow)


class StudentProgressHistory(Base):
    """
    Stores progress over time for charts and trend analysis.
    """
    __tablename__ = "student_progress_history"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Date for the progress entry
    date = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Daily stats
    exams_taken_today = Column(Integer, default=0)
    score_today = Column(Float, default=0.0)
    questions_attempted_today = Column(Integer, default=0)
    correct_answers_today = Column(Integer, default=0)
    study_time_minutes = Column(Integer, default=0)
    
    # Cumulative stats as of this date
    cumulative_exams = Column(Integer, default=0)
    cumulative_average = Column(Float, default=0.0)


class AIRecommendation(Base):
    """
    Stores AI-generated recommendations for each student.
    """
    __tablename__ = "ai_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Recommendation details
    recommendation_type = Column(String(50), nullable=False)  # 'weak_topic', 'improving', 'practice', 'advance'
    priority = Column(Integer, default=1)  # 1=High, 2=Medium, 3=Low
    
    sector_id = Column(Integer, ForeignKey("sectors.id"), nullable=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=True)
    
    sector_name = Column(String(150), nullable=True)
    section_name = Column(String(150), nullable=True)
    
    # Recommendation message
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Metrics that triggered this recommendation
    trigger_data = Column(JSON, default=dict)
    
    # Status
    is_read = Column(Integer, default=0)
    is_actioned = Column(Integer, default=0)
    
    # Created at
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sector = relationship("SectorModel")
    section = relationship("SectionModel")
