# section_feedback_router.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from typing import List, Optional
from datetime import datetime, timedelta

from database import get_db
from auth import get_current_user
from app.models.user_models import User
from app.models.section_models import SectionModel
from app.models.exam_models import ExamModel
from app.models.sector_models import SectorModel
from app.models.section_feedback_models import SectionRating, SectionFeedback
from app.schemas.section_feedback_schemas import (
    SectionRatingCreate,
    SectionRatingResponse,
    SectionFeedbackCreate,
    SectionFeedbackResponse,
    SectionWithRatings,
    FeedbackStats,
    SubmitFeedbackRequest,
    SubmitFeedbackResponse,
    SectionFeedbackWithSection,
    FeedbackModerateRequest,
    FeedbackModerateResponse,
    FeedbackListResponse,
    ExportFeedbackRequest
)

router = APIRouter(prefix="/api/section-feedback", tags=["Section Feedback"])


# ==================== GET SECTIONS WITH RATINGS ====================

@router.get("/sections", response_model=List[SectionWithRatings])
def get_sections_with_ratings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all sections with their ratings.
    Returns all sections (not filtered by grade) and includes user's grade.
    """
    # Check if user is student or eduoffice
    if current_user.role not in ['student', 'eduoffice']:
        raise HTTPException(status_code=403, detail="Access denied")
    # Get user's grade from their profile
    user_grade = current_user.grade or 0

    # Query all sections with their exams and sectors
    query = db.query(
        SectionModel.id.label('section_id'),
        SectionModel.name.label('section_name'),
        ExamModel.name.label('exam_title'),
        SectorModel.name.label('sector_name'),
        SectorModel.icon.label('sector_icon'),
        SectionModel.question_count,
        ExamModel.id.label('exam_id')
    ).join(
        ExamModel, SectionModel.exam_id == ExamModel.id
    ).join(
        SectorModel, ExamModel.sector_id == SectorModel.id
    )

    sections = query.all()

    # Build response with ratings
    result = []
    for section in sections:
        # Calculate average rating
        rating_stats = db.query(
            func.avg(SectionRating.rating).label('avg'),
            func.count(SectionRating.id).label('count')
        ).filter(SectionRating.section_id == section.section_id).first()

        avg_rating = float(rating_stats.avg) if rating_stats.avg else 0.0
        total_ratings = rating_stats.count or 0

        # Get user's rating if exists
        user_rating = db.query(SectionRating).filter(
            SectionRating.section_id == section.section_id,
            SectionRating.user_id == current_user.id
        ).first()

        result.append(SectionWithRatings(
            section_id=section.section_id,
            section_name=section.section_name,
            exam_title=section.exam_title,
            sector_name=section.sector_name,
            sector_icon=section.sector_icon,
            question_count=section.question_count,
            grade_level=user_grade,
            average_rating=round(avg_rating, 1),
            total_ratings=total_ratings,
            user_rating=user_rating.rating if user_rating else None
        ))

    return result


# ==================== RATE SECTION ====================

@router.post("/rate/{section_id}", response_model=SectionRatingResponse)
def rate_section(
    section_id: int,
    rating_data: SectionRatingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rate a section (1-5 stars).
    If already rated, updates the existing rating.
    """
    # Check if user is student (for rating sections)
    if current_user.role != 'student':
        raise HTTPException(status_code=403, detail="Only students can rate sections")
    # Verify section exists
    section = db.query(SectionModel).filter(SectionModel.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    # Check if user already rated this section
    existing_rating = db.query(SectionRating).filter(
        SectionRating.section_id == section_id,
        SectionRating.user_id == current_user.id
    ).first()

    if existing_rating:
        # Update existing rating
        existing_rating.rating = rating_data.rating
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    else:
        # Create new rating
        new_rating = SectionRating(
            section_id=section_id,
            user_id=current_user.id,
            rating=rating_data.rating
        )
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        return new_rating


# ==================== SUBMIT FEEDBACK ====================

@router.post("/feedback/{section_id}", response_model=SubmitFeedbackResponse)
def submit_feedback(
    section_id: int,
    feedback_data: SubmitFeedbackRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit feedback for a section.
    Can include rating and/or feedback text.
    Anonymous if is_anonymous is True.
    """
    # Check if user is student (for submitting feedback)
    if current_user.role != 'student':
        raise HTTPException(status_code=403, detail="Only students can submit feedback")
    # Verify section exists
    section = db.query(SectionModel).filter(SectionModel.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    rating_submitted = False
    feedback_submitted = False

    # Handle rating if provided
    if feedback_data.rating is not None:
        existing_rating = db.query(SectionRating).filter(
            SectionRating.section_id == section_id,
            SectionRating.user_id == current_user.id
        ).first()

        if existing_rating:
            existing_rating.rating = feedback_data.rating
        else:
            new_rating = SectionRating(
                section_id=section_id,
                user_id=current_user.id,
                rating=feedback_data.rating
            )
            db.add(new_rating)
        
        rating_submitted = True

    # Handle feedback text if provided
    if feedback_data.feedback_text and feedback_data.feedback_text.strip():
        feedback = SectionFeedback(
            section_id=section_id,
            user_id=None if feedback_data.is_anonymous else current_user.id,
            feedback_text=feedback_data.feedback_text.strip(),
            is_anonymous=feedback_data.is_anonymous
        )
        db.add(feedback)
        feedback_submitted = True

    db.commit()

    return SubmitFeedbackResponse(
        success=True,
        message="Feedback submitted successfully",
        rating_submitted=rating_submitted,
        feedback_submitted=feedback_submitted
    )


# ==================== GET SECTION DETAILS ====================

@router.get("/section/{section_id}", response_model=SectionWithRatings)
def get_section_details(
    section_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific section"""
    # Check if user is student (for viewing section details)
    if current_user.role != 'student':
        raise HTTPException(status_code=404, detail="Section not found")
    section = db.query(SectionModel).filter(SectionModel.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    exam = db.query(ExamModel).filter(ExamModel.id == section.exam_id).first()
    sector = db.query(SectorModel).filter(SectorModel.id == exam.sector_id).first()

    # Calculate average rating
    rating_stats = db.query(
        func.avg(SectionRating.rating).label('avg'),
        func.count(SectionRating.id).label('count')
    ).filter(SectionRating.section_id == section_id).first()

    avg_rating = float(rating_stats.avg) if rating_stats.avg else 0.0
    total_ratings = rating_stats.count or 0

    # Get user's rating
    user_rating = db.query(SectionRating).filter(
        SectionRating.section_id == section_id,
        SectionRating.user_id == current_user.id
    ).first()

    # Get user's grade from their profile
    user_grade = current_user.grade or 0

    return SectionWithRatings(
        section_id=section.id,
        section_name=section.name,
        exam_title=exam.name if exam else "",
        sector_name=sector.name if sector else "",
        sector_icon=sector.icon if sector else None,
        question_count=section.question_count,
        grade_level=user_grade,
        average_rating=round(avg_rating, 1),
        total_ratings=total_ratings,
        user_rating=user_rating.rating if user_rating else None
    )


# ==================== GET FEEDBACK STATS ====================

@router.get("/stats", response_model=FeedbackStats)
def get_feedback_stats(
    section_id: Optional[int] = Query(None, description="Filter by section ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get feedback statistics"""
    # Check if user is student or eduoffice
    if current_user.role not in ['student', 'eduoffice']:
        raise HTTPException(status_code=403, detail="Access denied")
    # Base query
    query = db.query(SectionFeedback)

    # Filter by section if provided
    if section_id:
        query = query.filter(SectionFeedback.section_id == section_id)

    # Get total count
    total_feedbacks = query.count()

    # Get today's count
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_feedbacks = query.filter(SectionFeedback.created_at >= today_start).count()

    # Get anonymous count
    anonymous_count = query.filter(SectionFeedback.is_anonymous == True).count()

    # Get recent feedbacks
    recent = query.order_by(SectionFeedback.created_at.desc()).limit(10).all()

    return FeedbackStats(
        total_feedbacks=total_feedbacks,
        today_feedbacks=today_feedbacks,
        anonymous_count=anonymous_count,
        recent_feedbacks=recent
    )


# ==================== GET ALL FEEDBACK (Admin/Teacher) ====================

@router.get("/all-feedback", response_model=List[SectionFeedbackWithSection])
def get_all_feedback(
    section_id: Optional[int] = Query(None),
    limit: int = Query(50, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all feedback (eduoffice only).
    Only returns non-anonymous feedback user info.
    """
    # Check if user is eduoffice
    if current_user.role != 'eduoffice':
        raise HTTPException(status_code=403, detail="Access denied")

    query = db.query(SectionFeedback)

    if section_id:
        query = query.filter(SectionFeedback.section_id == section_id)

    feedbacks = query.order_by(SectionFeedback.created_at.desc()).limit(limit).all()

    result = []
    for fb in feedbacks:
        section = db.query(SectionModel).filter(SectionModel.id == fb.section_id).first()
        exam = db.query(ExamModel).filter(ExamModel.id == section.exam_id).first() if section else None

        result.append(SectionFeedbackWithSection(
            id=fb.id,
            section_id=fb.section_id,
            user_id=fb.user_id if not fb.is_anonymous else None,
            feedback_text=fb.feedback_text,
            is_anonymous=fb.is_anonymous,
            created_at=fb.created_at,
            section_name=section.name if section else None,
            exam_title=exam.name if exam else None
        ))

    return result


# ==================== NEW FEEDBACK ENDPOINTS FOR DASHBOARD ====================

# ==================== GET FEEDBACK (Main Dashboard Endpoint) ====================

@router.get("/feedback", response_model=FeedbackListResponse)
def get_feedback(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    grade: Optional[int] = Query(None, description="Filter by grade level"),
    section: Optional[str] = Query(None, description="Filter by section name"),
    section_id: Optional[int] = Query(None, description="Filter by section ID"),
    rating: Optional[int] = Query(None, ge=1, le=5, description="Filter by rating"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    status: Optional[str] = Query(None, description="Filter by status: 'pending' or 'reviewed'"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get feedback list with role-based filtering.
    
    - TEACHER: Can only see feedback for their grade
    - EDU_OFFICE: Can see all feedback
    """
    # Check if user is teacher or eduoffice
    if current_user.role not in ['teacher', 'eduoffice']:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Start with base query
    query = db.query(SectionFeedback)
    
    # Role-based filtering for teachers - only feedback from students in their teaching grade
    if current_user.role == 'teacher':
        teacher_grade = getattr(current_user, 'teaching_grade', None)
        if teacher_grade:
            # Only non-anonymous feedback from students in teacher's grade
            query = query.filter(
                and_(
                    SectionFeedback.user_id.is_not(None),
                    SectionFeedback.is_anonymous == False,
                    SectionFeedback.user_id.in_(
                        db.query(User.id).filter(User.grade == teacher_grade)
                    )
                )
            )
        else:
            # If no teaching grade, no feedback
            query = query.filter(False)
    
    # Apply additional filters
    if grade:
        # Filter feedback by users who have the specified grade
        students_in_grade = db.query(User.id).filter(
            User.grade == grade
        ).all()
        student_ids = [s.id for s in students_in_grade]
        if student_ids:
            query = query.filter(SectionFeedback.user_id.in_(student_ids))
        else:
            # No students in this grade, return empty result
            return FeedbackListResponse(
                feedback=[],
                total=0,
                page=page,
                per_page=per_page,
                total_pages=0,
                stats={
                    "total_feedback": 0,
                    "average_rating": 0,
                    "anonymous_count": 0,
                    "anonymous_percent": 0,
                    "pending_count": 0,
                    "reviewed_count": 0,
                    "this_week": 0,
                    "this_month": 0
                }
            )
    
    if section:
        # Filter by section name
        sections = db.query(SectionModel).filter(
            SectionModel.name.ilike(f"%{section}%")
        ).all()
        section_ids = [s.id for s in sections]
        if section_ids:
            query = query.filter(SectionFeedback.section_id.in_(section_ids))
    
    if section_id:
        query = query.filter(SectionFeedback.section_id == section_id)
    
    if rating:
        query = query.filter(SectionFeedback.rating == rating)
    
    if start_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(SectionFeedback.created_at >= start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            end = end.replace(hour=23, minute=59, second=59)
            query = query.filter(SectionFeedback.created_at <= end)
        except ValueError:
            pass
    
    if status:
        query = query.filter(SectionFeedback.status == status)
    
    # Get total count before pagination
    total = query.count()
    total_pages = (total + per_page - 1) // per_page
    
    # Apply pagination
    offset = (page - 1) * per_page
    feedbacks = query.order_by(SectionFeedback.created_at.desc()).offset(offset).limit(per_page).all()
    
    # Build response with user info
    result = []
    for fb in feedbacks:
        section = db.query(SectionModel).filter(SectionModel.id == fb.section_id).first()
        
        # Get user info if not anonymous
        student_name = None
        username = None
        grade_level = None
        
        if not fb.is_anonymous and fb.user_id:
            user = db.query(User).filter(User.id == fb.user_id).first()
            if user:
                student_name = getattr(user, 'full_name', None) or getattr(user, 'username', None)
                username = getattr(user, 'username', None)
                grade_level = getattr(user, 'grade', None)
        
        # Get section name
        section_name = section.name if section else None
        
        result.append(FeedbackModerateResponse(
            id=fb.id,
            section_id=fb.section_id,
            user_id=fb.user_id if not fb.is_anonymous else None,
            feedback_text=fb.feedback_text,
            is_anonymous=fb.is_anonymous,
            rating=fb.rating,
            status=fb.status or "pending",
            internal_notes=fb.internal_notes,
            created_at=fb.created_at,
            updated_at=fb.updated_at,
            student_name=student_name,
            username=username,
            grade_level=grade_level,
            section_name=section_name
        ))
    
    # Calculate stats
    stats = _calculate_feedback_stats(query, db)
    
    return FeedbackListResponse(
        feedback=result,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        stats=stats
    )


def _calculate_feedback_stats(query, db):
    """Calculate feedback statistics"""
    # Get all feedbacks matching current filters
    all_feedbacks = query.all()
    
    total = len(all_feedbacks)
    anonymous_count = sum(1 for f in all_feedbacks if f.is_anonymous)
    pending_count = sum(1 for f in all_feedbacks if f.status != "reviewed")
    reviewed_count = sum(1 for f in all_feedbacks if f.status == "reviewed")
    
    # Calculate average rating
    ratings = [f.rating for f in all_feedbacks if f.rating is not None]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    # This week
    week_ago = datetime.utcnow() - timedelta(days=7)
    this_week = sum(1 for f in all_feedbacks if f.created_at >= week_ago)
    
    # This month
    month_ago = datetime.utcnow() - timedelta(days=30)
    this_month = sum(1 for f in all_feedbacks if f.created_at >= month_ago)
    
    return {
        "totalFeedback": total,
        "averageRating": round(avg_rating, 1),
        "anonymousCount": anonymous_count,
        "anonymousPercent": round((anonymous_count / total * 100) if total > 0 else 0, 1),
        "pendingCount": pending_count,
        "reviewedCount": reviewed_count,
        "thisWeek": this_week,
        "thisMonth": this_month
    }


# ==================== MODERATE FEEDBACK (PUT) ====================

@router.put("/moderate/{feedback_id}", response_model=FeedbackModerateResponse)
def moderate_feedback(
    feedback_id: int,
    moderate_data: FeedbackModerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Moderate feedback (edit, update status, add notes).
    Available for edu_office and admin roles only.
    """
    # Check if user is eduoffice
    if current_user.role != 'eduoffice':
        raise HTTPException(status_code=403, detail="Only eduoffice can moderate feedback")
    
    # Get feedback
    feedback = db.query(SectionFeedback).filter(SectionFeedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    # Update fields
    if moderate_data.feedback_text is not None:
        feedback.feedback_text = moderate_data.feedback_text
    
    if moderate_data.rating is not None:
        feedback.rating = moderate_data.rating
    
    if moderate_data.status is not None:
        if moderate_data.status not in ['pending', 'reviewed']:
            raise HTTPException(status_code=400, detail="Status must be 'pending' or 'reviewed'")
        feedback.status = moderate_data.status
    
    if moderate_data.internal_notes is not None:
        feedback.internal_notes = moderate_data.internal_notes
    
    feedback.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(feedback)
    
    # Get section
    section = db.query(SectionModel).filter(SectionModel.id == feedback.section_id).first()
    
    # Get user info if not anonymous
    student_name = None
    username = None
    grade_level = None
    
    if not feedback.is_anonymous and feedback.user_id:
        user = db.query(User).filter(User.id == feedback.user_id).first()
        if user:
            student_name = getattr(user, 'full_name', None) or getattr(user, 'username', None)
            username = getattr(user, 'username', None)
            grade_level = getattr(user, 'grade', None)
    
    return FeedbackModerateResponse(
        id=feedback.id,
        section_id=feedback.section_id,
        user_id=feedback.user_id if not feedback.is_anonymous else None,
        feedback_text=feedback.feedback_text,
        is_anonymous=feedback.is_anonymous,
        rating=feedback.rating,
        status=feedback.status or "pending",
        internal_notes=feedback.internal_notes,
        created_at=feedback.created_at,
        updated_at=feedback.updated_at,
        student_name=student_name,
        username=username,
        grade_level=grade_level,
        section_name=section.name if section else None
    )


# ==================== DELETE FEEDBACK ====================



@router.delete("/moderate/{feedback_id}")
def delete_feedback(
    feedback_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete feedback.
    Available for edu_office and admin roles only.
    """
    # Check if user is eduoffice
    if current_user.role != 'eduoffice':
        raise HTTPException(status_code=403, detail="Only eduoffice can delete feedback")
    
    # Get feedback
    feedback = db.query(SectionFeedback).filter(SectionFeedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    # Delete feedback
    db.delete(feedback)
    db.commit()
    
    return {"success": True, "message": "Feedback deleted successfully"}


# ==================== STUDENT MY FEEDBACK ENDPOINTS ====================

@router.get("/my-feedback", response_model=List[FeedbackModerateResponse])
def get_my_feedback(
    section_id: Optional[int] = Query(None, description="Optional: Filter by section"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current student's own non-anonymous feedback with status.
    """
    # Only own non-anonymous feedback
    query = db.query(SectionFeedback).filter(
        SectionFeedback.user_id == current_user.id,
        SectionFeedback.is_anonymous == False
    )
    
    if section_id:
        query = query.filter(SectionFeedback.section_id == section_id)
    
    feedbacks = query.order_by(SectionFeedback.created_at.desc()).all()
    
    result = []
    for fb in feedbacks:
        section = db.query(SectionModel).filter(SectionModel.id == fb.section_id).first()
        
        result.append(FeedbackModerateResponse(
            id=fb.id,
            section_id=fb.section_id,
            user_id=fb.user_id,
            feedback_text=fb.feedback_text,
            is_anonymous=fb.is_anonymous,
            rating=fb.rating,
            status=fb.status or "pending",
            internal_notes=fb.internal_notes,
            created_at=fb.created_at,
            updated_at=fb.updated_at,
            student_name=current_user.full_name or current_user.username,
            username=current_user.username,
            grade_level=current_user.grade,
            section_name=section.name if section else None
        ))
    
    return result


@router.put("/my-feedback/{feedback_id}", response_model=FeedbackModerateResponse)
def edit_my_feedback(
    feedback_id: int,
    update_data: FeedbackModerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Edit current student's own feedback (rating/text).
    """
    feedback = db.query(SectionFeedback).filter(
        SectionFeedback.id == feedback_id,
        SectionFeedback.user_id == current_user.id,
        SectionFeedback.is_anonymous == False
    ).first()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Own feedback not found")
    
    # Update fields
    if update_data.feedback_text is not None:
        feedback.feedback_text = update_data.feedback_text
    if update_data.rating is not None:
        feedback.rating = update_data.rating
    
    feedback.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(feedback)
    
    # Build response
    section = db.query(SectionModel).filter(SectionModel.id == feedback.section_id).first()
    return FeedbackModerateResponse(
        id=feedback.id,
        section_id=feedback.section_id,
        user_id=feedback.user_id,
        feedback_text=feedback.feedback_text,
        is_anonymous=feedback.is_anonymous,
        rating=feedback.rating,
        status=feedback.status or "pending",
        internal_notes=feedback.internal_notes,
        created_at=feedback.created_at,
        updated_at=feedback.updated_at,
        student_name=current_user.full_name or current_user.username,
        username=current_user.username,
        grade_level=current_user.grade,
        section_name=section.name if section else None
    )


@router.delete("/my-feedback/{feedback_id}")
def delete_my_feedback(
    feedback_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete current student's own feedback.
    """
    feedback = db.query(SectionFeedback).filter(
        SectionFeedback.id == feedback_id,
        SectionFeedback.user_id == current_user.id,
        SectionFeedback.is_anonymous == False
    ).first()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Own feedback not found")
    
    db.delete(feedback)
    db.commit()
    
    return {"success": True, "message": "Your feedback deleted successfully"}


# ==================== EXPORT FEEDBACK ====================


@router.get("/export")
def export_feedback(
    format: str = Query(..., description="Export format: 'pdf' or 'excel'"),
    grade: Optional[int] = Query(None, description="Filter by grade level"),
    section: Optional[str] = Query(None, description="Filter by section name"),
    rating: Optional[int] = Query(None, ge=1, le=5, description="Filter by rating"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    include_anonymous: bool = Query(True, description="Include anonymous feedback"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export feedback data.
    Available for edu_office and admin roles only.
    Returns data that can be used to generate PDF/Excel reports.
    """
    # Check if user is eduoffice
    if current_user.role != 'eduoffice':
        raise HTTPException(status_code=403, detail="Only eduoffice can export feedback")
    
    # Start with base query
    query = db.query(SectionFeedback)
    
    # Apply filters
    if grade:
        # Filter feedback by users who have the specified grade
        students_in_grade = db.query(User.id).filter(
            User.grade == grade
        ).all()
        student_ids = [s.id for s in students_in_grade]
        if student_ids:
            query = query.filter(SectionFeedback.user_id.in_(student_ids))
    
    if section:
        sections = db.query(SectionModel).filter(
            SectionModel.name.ilike(f"%{section}%")
        ).all()
        section_ids = [s.id for s in sections]
        if section_ids:
            query = query.filter(SectionFeedback.section_id.in_(section_ids))
    
    if rating:
        query = query.filter(SectionFeedback.rating == rating)
    
    if start_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(SectionFeedback.created_at >= start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            end = end.replace(hour=23, minute=59, second=59)
            query = query.filter(SectionFeedback.created_at <= end)
        except ValueError:
            pass
    
    if not include_anonymous:
        query = query.filter(SectionFeedback.is_anonymous == False)
    
    # Get all feedbacks
    feedbacks = query.order_by(SectionFeedback.created_at.desc()).all()
    
    # Build export data
    export_data = []
    for fb in feedbacks:
        section = db.query(SectionModel).filter(SectionModel.id == fb.section_id).first()
        
        # Get user info if not anonymous
        student_name = "Anonymous" if fb.is_anonymous else ""
        username = ""
        grade_level = ""
        
        if not fb.is_anonymous and fb.user_id:
            user = db.query(User).filter(User.id == fb.user_id).first()
            if user:
                student_name = getattr(user, 'full_name', None) or getattr(user, 'username', None) or "Unknown"
                username = getattr(user, 'username', None) or ""
                grade_level = str(getattr(user, 'grade', '')) or ""
        
        export_data.append({
            "id": fb.id,
            "student_name": student_name,
            "username": username,
            "grade_level": grade_level,
            "section_name": section.name if section else "",
            "rating": fb.rating,
            "feedback_text": fb.feedback_text,
            "is_anonymous": fb.is_anonymous,
            "status": fb.status or "pending",
            "created_at": fb.created_at.strftime("%Y-%m-%d %H:%M:%S") if fb.created_at else ""
        })
    
    # Calculate stats
    stats = _calculate_feedback_stats(query, db)
    
    return {
        "success": True,
        "format": format,
        "total": len(export_data),
        "data": export_data,
        "stats": stats,
        "filters": {
            "grade": grade,
            "section": section,
            "rating": rating,
            "start_date": start_date,
            "end_date": end_date,
            "include_anonymous": include_anonymous
        }
    }


# ==================== GET SECTIONS LIST ====================

@router.get("/sections-list")
def get_sections_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of all sections for filtering.
    """
    # Check if user is eduoffice
    if current_user.role != 'eduoffice':
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get all sections with their info
    sections = db.query(SectionModel).all()
    
    result = []
    for section in sections:
        exam = db.query(ExamModel).filter(ExamModel.id == section.exam_id).first() if section.exam_id else None
        
        # Calculate average rating for this section
        ratings = db.query(SectionRating).filter(SectionRating.section_id == section.id).all()
        avg_rating = 0
        if ratings:
            avg_rating = sum(r.rating for r in ratings) / len(ratings)
        
        # Count feedback for this section
        feedback_count = db.query(SectionFeedback).filter(SectionFeedback.section_id == section.id).count()
        
        # Get grade info from users who gave feedback for this section (if not anonymous)
        section_grade = None
        feedback_with_grade = db.query(SectionFeedback).filter(
            SectionFeedback.section_id == section.id,
            SectionFeedback.is_anonymous == False,
            SectionFeedback.user_id.isnot(None)
        ).limit(10).all()
        
        if feedback_with_grade:
            # Get grade from first non-anonymous user who gave feedback
            first_user = db.query(User).filter(User.id == feedback_with_grade[0].user_id).first()
            if first_user:
                section_grade = first_user.grade
        
        result.append({
            "id": section.id,
            "name": section.name,
            "grade_level": section_grade,
            "exam_title": exam.name if exam else None,
            "average_rating": round(avg_rating, 1),
            "total_ratings": len(ratings),
            "feedback_count": feedback_count
        })
    
    return result

