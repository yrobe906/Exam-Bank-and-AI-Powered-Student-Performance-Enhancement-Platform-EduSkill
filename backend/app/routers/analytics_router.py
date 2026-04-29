# analytics_router.py
# API Router for Performance Analytics Dashboard
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from app.crud import analytics_crud
from app.schemas import analytics_schemas

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


# ==================== DEBUG HEALTH CHECK ====================

@router.get("/health")
def analytics_health_check():
    """Debug endpoint to verify analytics router is working"""
    return {
        "status": "ok",
        "message": "Analytics router is working",
        "endpoints": [
            "/calculate/{student_id}",
            "/student/{student_id}/summary",
            "/student/{student_id}/subjects",
            "/student/{student_id}/topics",
            "/student/{student_id}/dashboard",
            "/student/{student_id}/weak-topics",
            "/student/{student_id}/progress",
            "/student/{student_id}/recommendations",
            "/recalculate-all",
            "/recalculate-student/{student_id}"
        ]
    }


# ==================== HELPER DEPENDENCIES ====================

def get_current_student_id(student_id: int) -> int:
    """Dependency to get current student ID"""
    # In a real app, this would verify the user is authenticated
    # For now, we accept student_id as a parameter
    return student_id


# ==================== MAIN ANALYTICS ENDPOINTS ====================

@router.post("/calculate/{student_id}", response_model=analytics_schemas.CalculateAnalyticsResponse)
def calculate_analytics(
    student_id: int,
    request: analytics_schemas.CalculateAnalyticsRequest = None,
    db: Session = Depends(get_db)
):
    """
    Calculate/refresh analytics for a student.
    This endpoint triggers the calculation of all analytics data.
    Use force_refresh=true to recalculate even if recent data exists.
    """
    force_refresh = request.force_refresh if request else False
    
    result = analytics_crud.calculate_all_analytics(db, student_id, force_refresh)
    
    return analytics_schemas.CalculateAnalyticsResponse(
        student_id=student_id,
        success=result.get('success', True),
        message=result.get('message', 'Calculated successfully'),
        calculated_subjects=result.get('calculated_subjects', 0),
        calculated_topics=result.get('calculated_topics', 0),
        recommendations_generated=result.get('recommendations_generated', 0),
        calculated_at=result.get('calculated_at', datetime.utcnow())
    )


@router.get("/student/{student_id}/summary", response_model=analytics_schemas.OverallSummaryResponse)
def get_student_summary(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get overall performance summary for a student.
    Returns key metrics like average score, exams taken, weak topics count, etc.
    """
    # Get overall analytics
    overall = db.query(analytics_crud.StudentOverallAnalytics).filter(
        analytics_crud.StudentOverallAnalytics.student_id == student_id
    ).first()
    
    if not overall:
        # Calculate if not exists
        analytics_crud.calculate_all_analytics(db, student_id, force_refresh=True)
        overall = db.query(analytics_crud.StudentOverallAnalytics).filter(
            analytics_crud.StudentOverallAnalytics.student_id == student_id
        ).first()
        
        if not overall:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No analytics data found for this student"
            )
    
    return analytics_schemas.OverallSummaryResponse(
        student_id=overall.student_id,
        total_exams_taken=overall.total_exams_taken,
        average_score=overall.average_score,
        highest_score=overall.highest_score,
        lowest_score=overall.lowest_score,
        total_study_time_minutes=overall.total_study_time_minutes,
        total_subjects_studied=overall.total_subjects_studied,
        total_topics_covered=overall.total_topics_covered,
        weak_topics_count=overall.weak_topics_count,
        class_rank=overall.class_rank,
        calculated_at=overall.calculated_at
    )


@router.get("/student/{student_id}/subjects", response_model=List[analytics_schemas.SubjectAnalyticsResponse])
def get_subject_analytics(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get subject-wise performance for a student.
    Returns scores and metrics broken down by subject/sector.
    """
    # Ensure analytics are calculated
    analytics_crud.calculate_all_analytics(db, student_id, force_refresh=False)
    
    subjects = analytics_crud.get_subject_analytics(db, student_id)
    
    return [
        analytics_schemas.SubjectAnalyticsResponse(
            id=s.id,
            sector_id=s.sector_id,
            sector_name=s.sector_name,
            total_exams_taken=s.total_exams_taken,
            average_score=s.average_score,
            highest_score=s.highest_score,
            lowest_score=s.lowest_score,
            total_questions_attempted=s.total_questions_attempted,
            total_correct_answers=s.total_correct_answers,
            accuracy_percentage=analytics_crud.calculate_accuracy(
                s.total_correct_answers, 
                s.total_questions_attempted
            ) if s.total_questions_attempted > 0 else 0.0,
            calculated_at=s.calculated_at
        )
        for s in subjects
    ]


@router.get("/student/{student_id}/topics", response_model=List[analytics_schemas.TopicAnalyticsResponse])
def get_topic_analytics(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get topic-wise performance for a student.
    Returns scores and metrics broken down by topic/section.
    """
    # Ensure analytics are calculated
    analytics_crud.calculate_all_analytics(db, student_id, force_refresh=False)
    
    topics = analytics_crud.get_topic_analytics(db, student_id)
    
    return [
        analytics_schemas.TopicAnalyticsResponse(
            id=t.id,
            section_id=t.section_id,
            section_name=t.section_name,
            sector_id=t.sector_id,
            sector_name=t.sector_name,
            total_exams_taken=t.total_exams_taken,
            average_score=t.average_score,
            total_questions_attempted=t.total_questions_attempted,
            total_correct_answers=t.total_correct_answers,
            accuracy_percentage=analytics_crud.calculate_accuracy(
                t.total_correct_answers,
                t.total_questions_attempted
            ) if t.total_questions_attempted > 0 else 0.0,
            recent_scores=t.recent_scores or [],
            is_weak_topic=bool(t.is_weak_topic),
            weakness_level=t.weakness_level,
            calculated_at=t.calculated_at
        )
        for t in topics
    ]


@router.get("/student/{student_id}/progress", response_model=analytics_schemas.ProgressHistoryResponse)
def get_progress_history(
    student_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get progress history for charts.
    Returns daily progress data for the specified number of days.
    """
    # Ensure analytics are calculated
    analytics_crud.calculate_all_analytics(db, student_id, force_refresh=False)
    
    progress = analytics_crud.get_progress_history(db, student_id, days)
    
    progress_data = [
        analytics_schemas.ProgressEntry(
            date=p.date.strftime('%Y-%m-%d') if isinstance(p.date, datetime) else str(p.date),
            exams_taken=p.exams_taken_today,
            score=p.score_today,
            questions_attempted=p.questions_attempted_today,
            correct_answers=p.correct_answers_today,
            accuracy=analytics_crud.calculate_accuracy(
                p.correct_answers_today,
                p.questions_attempted_today
            ) if p.questions_attempted_today > 0 else 0.0,
            study_time_minutes=p.study_time_minutes
        )
        for p in progress
    ]
    
    return analytics_schemas.ProgressHistoryResponse(
        student_id=student_id,
        progress_data=progress_data,
        total_entries=len(progress_data)
    )


@router.get("/student/{student_id}/weak-topics", response_model=analytics_schemas.WeakTopicsListResponse)
def get_weak_topics(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get AI-detected weak topics for a student.
    Returns topics where the student is struggling based on exam performance.
    """
    # Ensure analytics are calculated
    analytics_crud.calculate_all_analytics(db, student_id, force_refresh=False)
    
    weak_topics = analytics_crud.get_weak_topics(db, student_id)
    
    weak_topics_list = [
        analytics_schemas.WeakTopicResponse(
            section_id=t.section_id,
            section_name=t.section_name,
            sector_id=t.sector_id,
            sector_name=t.sector_name,
            average_score=t.average_score,
            recent_scores=t.recent_scores or [],
            weakness_level=t.weakness_level,
            exam_count=t.total_exams_taken,
            trend=analytics_crud.analyze_trend(t.recent_scores or []),
            recommendation=_get_weakness_recommendation(t.average_score, t.weakness_level)
        )
        for t in weak_topics
    ]
    
    return analytics_schemas.WeakTopicsListResponse(
        student_id=student_id,
        weak_topics=weak_topics_list,
        total_weak_topics=len(weak_topics_list)
    )


def _get_weakness_recommendation(average_score: float, weakness_level: int) -> str:
    """Generate recommendation text based on weakness level"""
    if weakness_level == 3:  # Severe
        return f"Urgent: Focus on fundamentals. Score: {average_score:.1f}%"
    elif weakness_level == 2:  # Moderate
        return f"Need practice. Target: 70%+. Current: {average_score:.1f}%"
    else:  # Mild
        return f"Almost there! Aim for 80%+. Current: {average_score:.1f}%"


@router.get("/student/{student_id}/recommendations", response_model=analytics_schemas.RecommendationsListResponse)
def get_recommendations(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get AI-generated recommendations for a student.
    Returns personalized learning suggestions based on performance.
    """
    # Ensure analytics are calculated
    analytics_crud.calculate_all_analytics(db, student_id, force_refresh=False)
    
    recommendations = analytics_crud.get_recommendations(db, student_id)
    
    high_priority = sum(1 for r in recommendations if r.priority == 1)
    
    rec_list = [
        analytics_schemas.AIRecommendationResponse(
            id=r.id,
            recommendation_type=r.recommendation_type,
            priority=r.priority,
            title=r.title,
            description=r.description,
            sector_id=r.sector_id,
            section_id=r.section_id,
            sector_name=r.sector_name,
            section_name=r.section_name,
            is_read=bool(r.is_read),
            is_actioned=bool(r.is_actioned),
            created_at=r.created_at,
            trigger_data=r.trigger_data or {}
        )
        for r in recommendations
    ]
    
    return analytics_schemas.RecommendationsListResponse(
        student_id=student_id,
        recommendations=rec_list,
        total_recommendations=len(rec_list),
        high_priority_count=high_priority
    )


@router.get("/student/{student_id}/dashboard", response_model=analytics_schemas.DashboardSummaryResponse)
def get_dashboard_summary(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get complete dashboard summary.
    This is the main endpoint for the Performance Analytics Dashboard.
    Returns all data needed for the frontend in a single call.
    """
    # Ensure analytics are calculated
    analytics_crud.calculate_all_analytics(db, student_id, force_refresh=False)
    
    # Get dashboard data
    dashboard_data = analytics_crud.get_dashboard_summary(db, student_id)
    
    # Get overall for quick stats
    overall = db.query(analytics_crud.StudentOverallAnalytics).filter(
        analytics_crud.StudentOverallAnalytics.student_id == student_id
    ).first()
    
    # Get strongest and weakest topics
    all_topics = analytics_crud.get_topic_analytics(db, student_id)
    strongest = all_topics[-1] if all_topics else None
    weakest = all_topics[0] if all_topics and all_topics[0].average_score < 70 else None
    
    # Get flashcard and practice mock stats
    flashcard_stats = dashboard_data.get('flashcard_stats', {})
    practice_mock_stats = dashboard_data.get('practice_mock_stats', {})
    
    return analytics_schemas.DashboardSummaryResponse(
        student_id=student_id,
        average_score=dashboard_data.get('average_score', 0),
        total_exams_taken=dashboard_data.get('total_exams_taken', 0),
        weak_topics_count=dashboard_data.get('weak_topics_count', 0),
        class_rank=dashboard_data.get('class_rank'),
        score_change=0.0,  # TODO: Calculate from previous period
        exams_change=0,    # TODO: Calculate from previous period
        subjects=[
            analytics_schemas.SubjectAnalyticsBase(
                sector_id=s['sector_id'],
                sector_name=s['sector_name'],
                total_exams_taken=s['total_exams_taken'],
                average_score=s['average_score'],
                highest_score=s['highest_score'],
                lowest_score=s['lowest_score'],
                total_questions_attempted=s['total_questions_attempted'],
                total_correct_answers=s['total_correct_answers'],
                accuracy_percentage=s['accuracy_percentage']
            )
            for s in dashboard_data.get('subjects', [])
        ],
        strongest_topic=analytics_schemas.TopicAnalyticsBase(
            section_id=strongest.section_id,
            section_name=strongest.section_name,
            sector_id=strongest.sector_id,
            sector_name=strongest.sector_name,
            total_exams_taken=strongest.total_exams_taken,
            average_score=strongest.average_score,
            total_questions_attempted=strongest.total_questions_attempted,
            total_correct_answers=strongest.total_correct_answers,
            accuracy_percentage=analytics_crud.calculate_accuracy(
                strongest.total_correct_answers,
                strongest.total_questions_attempted
            ) if strongest.total_questions_attempted > 0 else 0.0,
            recent_scores=strongest.recent_scores or [],
            is_weak_topic=bool(strongest.is_weak_topic),
            weakness_level=strongest.weakness_level
        ) if strongest else None,
        weakest_topic=analytics_schemas.TopicAnalyticsBase(
            section_id=weakest.section_id,
            section_name=weakest.section_name,
            sector_id=weakest.sector_id,
            sector_name=weakest.sector_name,
            total_exams_taken=weakest.total_exams_taken,
            average_score=weakest.average_score,
            total_questions_attempted=weakest.total_questions_attempted,
            total_correct_answers=weakest.total_correct_answers,
            accuracy_percentage=analytics_crud.calculate_accuracy(
                weakest.total_correct_answers,
                weakest.total_questions_attempted
            ) if weakest.total_questions_attempted > 0 else 0.0,
            recent_scores=weakest.recent_scores or [],
            is_weak_topic=bool(weakest.is_weak_topic),
            weakness_level=weakest.weakness_level
        ) if weakest else None,
        recent_recommendations=[
            analytics_schemas.AIRecommendationBase(
                recommendation_type=r['recommendation_type'],
                priority=r['priority'],
                title=r['title'],
                description=r['description'],
                sector_id=r.get('sector_id'),
                section_id=r.get('section_id'),
                sector_name=r.get('sector_name'),
                section_name=r.get('section_name')
            )
            for r in dashboard_data.get('recent_recommendations', [])
        ],
        weekly_progress=[
            analytics_schemas.ProgressEntry(
                date=p['date'],
                exams_taken=p['exams_taken'],
                score=p['score'],
                questions_attempted=p['questions_attempted'],
                correct_answers=p['correct_answers'],
                accuracy=p['accuracy'],
                study_time_minutes=p['study_time_minutes']
            )
            for p in dashboard_data.get('weekly_progress', [])
        ],
        flashcard_stats=analytics_schemas.FlashcardStats(
            total_cards_reviewed=flashcard_stats.get('total_cards_reviewed', 0),
            learning_count=flashcard_stats.get('learning_count', 0),
            known_count=flashcard_stats.get('known_count', 0),
            revisit_count=flashcard_stats.get('revisit_count', 0),
            total_reviews=flashcard_stats.get('total_reviews', 0),
            mastery_percentage=flashcard_stats.get('mastery_percentage', 0.0)
        ),
        practice_mock_stats=analytics_schemas.PracticeMockStats(
            total_tests_taken=practice_mock_stats.get('total_tests_taken', 0),
            average_score=practice_mock_stats.get('average_score', 0.0),
            highest_score=practice_mock_stats.get('highest_score', 0.0),
            lowest_score=practice_mock_stats.get('lowest_score', 0.0),
            total_questions_attempted=practice_mock_stats.get('total_questions_attempted', 0),
            total_correct=practice_mock_stats.get('total_correct', 0),
            subjects_practiced=practice_mock_stats.get('subjects_practiced', [])
        )
    )


# ==================== RECALCULATE ALL STUDENTS ANALYTICS ====================

@router.post("/recalculate-all")
def recalculate_all_students_analytics(
    db: Session = Depends(get_db)
):
    """
    Recalculate analytics for ALL students who have exam attempts.
    This endpoint is useful when:
    - Analytics were not being calculated after exam submissions (BUG FIX)
    - You want to refresh all student analytics
    - Initial setup after adding analytics feature
    
    Returns a summary of students processed and any errors encountered.
    """
    from app.models.exam_attempt_models import ExamAttemptModel
    from app.models.user_models import User
    
    # Get all unique student_ids who have at least one exam attempt
    student_ids_with_attempts = db.query(
        ExamAttemptModel.student_id
    ).distinct().all()
    
    student_ids = [s[0] for s in student_ids_with_attempts]
    
    if not student_ids:
        return {
            "success": True,
            "message": "No exam attempts found in the system",
            "students_processed": 0,
            "results": []
        }
    
    results = []
    errors = []
    successful = 0
    
    for student_id in student_ids:
        try:
            # Check if student exists
            student = db.query(User).filter(User.id == student_id).first()
            if not student:
                errors.append({
                    "student_id": student_id,
                    "error": "Student not found in users table"
                })
                continue
            
            # Calculate analytics with force refresh
            result = analytics_crud.calculate_all_analytics(db, student_id, force_refresh=True)
            
            results.append({
                "student_id": student_id,
                "success": True,
                "subjects_calculated": result.get('calculated_subjects', 0),
                "topics_calculated": result.get('calculated_topics', 0),
                "recommendations_generated": result.get('recommendations_generated', 0)
            })
            successful += 1
            
        except Exception as e:
            errors.append({
                "student_id": student_id,
                "error": str(e)
            })
            results.append({
                "student_id": student_id,
                "success": False,
                "error": str(e)
            })
    
    return {
        "success": True,
        "message": f"Analytics recalculation completed. {successful}/{len(student_ids)} students processed successfully.",
        "total_students_with_attempts": len(student_ids),
        "students_processed": successful,
        "students_with_errors": len(errors),
        "results": results,
        "errors": errors
    }


# ==================== RECALCULATE SPECIFIC STUDENT ANALYTICS ====================

@router.post("/recalculate-student/{student_id}")
def recalculate_student_analytics(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Recalculate analytics for a specific student.
    Use this to refresh analytics for a single student.
    """
    from app.models.exam_attempt_models import ExamAttemptModel
    from app.models.user_models import User
    
    # Check if student exists
    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    
    # Check if student has any exam attempts
    attempts = db.query(ExamAttemptModel).filter(
        ExamAttemptModel.student_id == student_id
    ).count()
    
    if attempts == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No exam attempts found for student id {student_id}"
        )
    
    # Calculate analytics
    result = analytics_crud.calculate_all_analytics(db, student_id, force_refresh=True)
    
    return {
        "success": True,
        "message": f"Analytics recalculated for student {student_id}",
        "student_id": student_id,
        "total_exam_attempts": attempts,
        "subjects_calculated": result.get('calculated_subjects', 0),
        "topics_calculated": result.get('calculated_topics', 0),
        "recommendations_generated": result.get('recommendations_generated', 0),
        "class_rank": analytics_crud.calculate_class_rank(db, student_id),
        "calculated_at": result.get('calculated_at', datetime.utcnow())
    }


# ==================== AVERAGE SCORE PER SECTION ====================

@router.get("/student/{student_id}/section-scores")
def get_section_scores(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get average score per section for a student.
    Returns section-wise performance data.
    """
    analytics_crud.calculate_all_analytics(db, student_id, force_refresh=False)
    section_scores = analytics_crud.get_section_wise_scores(db, student_id)
    
    return {
        "student_id": student_id,
        "section_count": len(section_scores),
        "sections": section_scores
    }


# ==================== AVERAGE SCORE ACROSS ALL EXAMS ====================

@router.get("/student/{student_id}/overall-average")
def get_overall_average(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get average score across all exams taken by the student.
    Formula: sum_of_all_exam_scores / total_exams_taken
    """
    attempts = analytics_crud.get_student_exam_attempts(db, student_id)
    
    if not attempts:
        return {
            "student_id": student_id,
            "total_exams_taken": 0,
            "average_score": 0.0,
            "message": "No exams taken yet"
        }
    
    all_scores = []
    for attempt in attempts:
        answers = analytics_crud.get_student_answers_for_exam(db, attempt.id)
        if answers:
            correct_count = sum(1 for a in answers if a.is_correct)
            percentage = (correct_count / len(answers)) * 100
            all_scores.append(percentage)
        else:
            all_scores.append(attempt.score)
    
    overall_avg = sum(all_scores) / len(all_scores) if all_scores else 0
    
    return {
        "student_id": student_id,
        "total_exams_taken": len(attempts),
        "average_score": round(overall_avg, 2),
        "highest_score": max(all_scores) if all_scores else 0,
        "lowest_score": min(all_scores) if all_scores else 0
    }


# ==================== EXAMS TAKEN COUNT ====================

@router.get("/student/{student_id}/exams-taken")
def get_exams_taken(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get total number of mock exams completed by user.
    """
    attempts = analytics_crud.get_student_exam_attempts(db, student_id)
    completed_attempts = [a for a in attempts if a.completed_at is not None]
    
    return {
        "student_id": student_id,
        "total_exams_taken": len(completed_attempts),
        "exams": [
            {
                "attempt_id": a.id,
                "exam_id": a.exam_id,
                "score": a.score,
                "completed_at": a.completed_at.strftime('%Y-%m-%d %H:%M:%S') if a.completed_at else None
            }
            for a in completed_attempts
        ]
    }


# ==================== SUBJECTS COVERED ====================

@router.get("/student/{student_id}/subjects-covered")
def get_subjects_covered(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get count of distinct sectors (subjects) from exams taken.
    """
    analytics_crud.calculate_all_analytics(db, student_id, force_refresh=False)
    subjects = analytics_crud.get_subject_analytics(db, student_id)
    
    return {
        "student_id": student_id,
        "subjects_covered": len(subjects),
        "subjects": [
            {
                "sector_id": s.sector_id,
                "sector_name": s.sector_name,
                "total_exams_taken": s.total_exams_taken
            }
            for s in subjects
        ]
    }


# ==================== CLASS RANK ====================

@router.get("/student/{student_id}/class-rank")
def get_class_rank(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get class rank for student among users of same grade.
    Ranking based on overall average score.
    """
    rank = analytics_crud.calculate_class_rank(db, student_id)
    
    from app.models.user_models import User
    student = db.query(User).filter(User.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    
    from app.models.exam_attempt_models import ExamAttemptModel
    students_in_grade = db.query(
        ExamAttemptModel.student_id
    ).join(
        User, ExamAttemptModel.student_id == User.id
    ).filter(
        User.grade == student.grade
    ).distinct().count()
    
    return {
        "student_id": student_id,
        "grade": student.grade,
        "class_rank": rank if rank else 1,
        "total_students_in_grade": students_in_grade,
        "note": "Default rank = 1 if no other student in same grade has taken exams"
    }


# ==================== WEAK TOPICS (50% THRESHOLD) ====================

@router.get("/student/{student_id}/weak-topics-50")
def get_weak_topics_50(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get weak topics where average score < 50%.
    Returns list sorted from weakest to strongest.
    """
    analytics_crud.calculate_all_analytics(db, student_id, force_refresh=False)
    all_topics = analytics_crud.get_topic_analytics(db, student_id)
    weak_topics = [t for t in all_topics if t.average_score < 50]
    weak_topics.sort(key=lambda x: x.average_score)
    
    return {
        "student_id": student_id,
        "weak_topics_count": len(weak_topics),
        "weak_topics": [
            {
                "section_id": t.section_id,
                "section_name": t.section_name,
                "sector_id": t.sector_id,
                "sector_name": t.sector_name,
                "average_score": t.average_score,
                "total_exams_taken": t.total_exams_taken,
                "recent_scores": t.recent_scores or []
            }
            for t in weak_topics
        ]
    }


# ==================== AI RECOMMENDATION PER EXAM ====================

@router.get("/student/{student_id}/exam-recommendation/{attempt_id}")
def get_exam_recommendation(
    student_id: int,
    attempt_id: int,
    db: Session = Depends(get_db)
):
    """
    Get AI recommendation for a specific exam attempt.
    Returns score, weak sections, and recommended exam type.
    """
    recommendation = analytics_crud.generate_per_exam_recommendation(db, student_id, attempt_id)
    
    return {
        "student_id": student_id,
        "attempt_id": attempt_id,
        "recommendation": recommendation
    }


# ==================== SECTION LEADERBOARD (BY SECTION) ====================

@router.get("/section-leaderboard")
def get_section_leaderboard(
    grade_level: int = None,
    section_category: str = None,
    db: Session = Depends(get_db)
):
    """
    Get section-level leaderboard ranking by unique section names.
    
    Groups all exams by their section names (e.g., "Chemistry", "English")
    and calculates aggregated metrics:
    - Total exam attempts across ALL exams in that section
    - Average student scores across ALL students who took exams in that section
    - Weighted score: (attempts * 0.6) + (avgScore * 0.4)
    
    Filters:
    - grade_level: Filter by student grade
    - section_category: Filter by section/sector name
    """
    from app.models import exam_models, section_models, sector_models
    from app.models.exam_attempt_models import ExamAttemptModel
    from app.models.user_models import User
    
    # Get all sections with their exam and sector info
    sections = db.query(
        section_models.SectionModel.id.label("section_id"),
        section_models.SectionModel.name.label("section_name"),
        section_models.SectionModel.color,
        exam_models.ExamModel.id.label("exam_id"),
        exam_models.ExamModel.name.label("exam_name"),
        sector_models.SectorModel.id.label("sector_id"),
        sector_models.SectorModel.name.label("sector_name"),
        sector_models.SectorModel.icon.label("sector_icon")
    ).join(
        exam_models.ExamModel, section_models.SectionModel.exam_id == exam_models.ExamModel.id
    ).join(
        sector_models.SectorModel, exam_models.ExamModel.sector_id == sector_models.SectorModel.id
    ).all()
    
    # Group exams by section name
    section_exams_map = {}
    for s in sections:
        section_name = s.section_name
        if section_name not in section_exams_map:
            section_exams_map[section_name] = {
                "section_id": s.section_id,
                "section_name": section_name,
                "color": s.color,
                "sector_id": s.sector_id,
                "sector_name": s.sector_name,
                "sector_icon": s.sector_icon,
                "exam_ids": set(),
                "exam_names": set()
            }
        section_exams_map[section_name]["exam_ids"].add(s.exam_id)
        section_exams_map[section_name]["exam_names"].add(s.exam_name)
    
    # Calculate metrics for each section
    section_data = []
    max_attempts = 1  # To avoid division by zero
    
    # First pass: find max attempts for normalization
    for section_name, data in section_exams_map.items():
        exam_ids = list(data["exam_ids"])
        
        attempt_query = db.query(
            ExamAttemptModel,
            User.grade
        ).join(
            User, ExamAttemptModel.student_id == User.id
        ).filter(
            ExamAttemptModel.exam_id.in_(exam_ids)
        )
        
        if grade_level:
            attempt_query = attempt_query.filter(User.grade == grade_level)
        
        attempts = attempt_query.all()
        valid_attempts = sum(1 for a, _ in attempts if a.completed_at is not None)
        max_attempts = max(max_attempts, valid_attempts)
    
    # Second pass: calculate normalized metrics
    for section_name, data in section_exams_map.items():
        exam_ids = list(data["exam_ids"])
        
        # Build query for exam attempts
        attempt_query = db.query(
            ExamAttemptModel,
            User.grade
        ).join(
            User, ExamAttemptModel.student_id == User.id
        ).filter(
            ExamAttemptModel.exam_id.in_(exam_ids)
        )
        
        # Apply grade filter
        if grade_level:
            attempt_query = attempt_query.filter(User.grade == grade_level)
        
        attempts = attempt_query.all()
        
        # Get unique students and calculate average score
        unique_students = set()
        total_score = 0
        valid_attempts = 0
        
        for attempt, student_grade in attempts:
            if attempt.completed_at is not None:  # Only completed attempts
                unique_students.add(attempt.student_id)
                total_score += attempt.score
                valid_attempts += 1
        
        # Average score - multiply by 100 to get percentage
        avg_score = (total_score / valid_attempts * 100) if valid_attempts > 0 else 0
        
        # Normalize attempts to be out of 100 (percentage)
        normalized_attempts = (valid_attempts / max_attempts * 100) if max_attempts > 0 else 0
        
        # Weighted score: (normalized_attempts * 0.6) + (avg_score * 0.4) - all out of 100
        weighted_score = (normalized_attempts * 0.6) + (avg_score * 0.4)
        
        # Apply section category filter
        if section_category and section_category.lower() != "all":
            if data["sector_name"].lower() != section_category.lower():
                continue
        
        section_data.append({
            "section_id": data["section_id"],
            "section_name": data["section_name"],
            "color": data["color"] or "#6366f1",
            "sector_id": data["sector_id"],
            "sector_name": data["sector_name"],
            "sector_icon": data["sector_icon"],
            "total_exam_attempts": valid_attempts,
            "max_attempts": max_attempts,
            "normalized_attempts": round(normalized_attempts, 2),
            "unique_students": len(unique_students),
            "average_score": round(avg_score, 2),
            "weighted_score": round(weighted_score, 2),
            "exams_count": len(data["exam_ids"]),
            "exam_names": list(data["exam_names"])[:5]  # Limit to 5 for display
        })
    
    # Sort by weighted score (descending) and add rank
    section_data.sort(key=lambda x: x["weighted_score"], reverse=True)
    for i, section in enumerate(section_data, 1):
        section["rank"] = i
    
    return {
        "total_sections": len(section_data),
        "grade_filter": grade_level,
        "category_filter": section_category,
        "sections": section_data
    }


# ==================== SECTION DETAIL (DRILL DOWN) ====================

@router.get("/section-leaderboard/{section_name}/details")
def get_section_details(
    section_name: str,
    grade_level: int = None,
    db: Session = Depends(get_db)
):
    """
    Get detailed information for a specific section.
    Returns all exams in that section and their individual performance.
    """
    from app.models import exam_models, section_models, sector_models
    from app.models.exam_attempt_models import ExamAttemptModel
    from app.models.user_models import User
    
    # Find all exams containing this section
    sections = db.query(
        section_models.SectionModel.id.label("section_id"),
        section_models.SectionModel.name.label("section_name"),
        exam_models.ExamModel.id.label("exam_id"),
        exam_models.ExamModel.name.label("exam_name"),
        exam_models.ExamModel.total_questions,
        exam_models.ExamModel.duration,
        sector_models.SectorModel.id.label("sector_id"),
        sector_models.SectorModel.name.label("sector_name")
    ).join(
        exam_models.ExamModel, section_models.SectionModel.exam_id == exam_models.ExamModel.id
    ).join(
        sector_models.SectorModel, exam_models.ExamModel.sector_id == sector_models.SectorModel.id
    ).filter(
        section_models.SectionModel.name == section_name
    ).all()
    
    if not sections:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section '{section_name}' not found"
        )
    
    # Get unique exam IDs
    exam_ids = list(set(s.exam_id for s in sections))
    
    # Calculate metrics for each exam
    exam_details = []
    for exam_id in exam_ids:
        exam_info = next((s for s in sections if s.exam_id == exam_id), None)
        if not exam_info:
            continue
            
        # Get attempts for this exam
        attempt_query = db.query(
            ExamAttemptModel,
            User.grade
        ).join(
            User, ExamAttemptModel.student_id == User.id
        ).filter(
            ExamAttemptModel.exam_id == exam_id
        )
        
        if grade_level:
            attempt_query = attempt_query.filter(User.grade == grade_level)
        
        attempts = attempt_query.all()
        
        # Calculate metrics
        unique_students = set()
        total_score = 0
        valid_attempts = 0
        
        for attempt, student_grade in attempts:
            if attempt.completed_at is not None:
                unique_students.add(attempt.student_id)
                total_score += attempt.score
                valid_attempts += 1
        
        avg_score = (total_score / valid_attempts * 100) if valid_attempts > 0 else 0
        
        exam_details.append({
            "exam_id": exam_id,
            "exam_name": exam_info.exam_name,
            "total_questions": exam_info.total_questions or 0,
            "duration": exam_info.duration or 0,
            "total_attempts": valid_attempts,
            "unique_students": len(unique_students),
            "average_score": round(avg_score, 2),
            "sector_name": exam_info.sector_name
        })
    
    # Sort by average score
    exam_details.sort(key=lambda x: x["average_score"], reverse=True)
    
    return {
        "section_name": section_name,
        "total_exams": len(exam_details),
        "exams": exam_details
    }


# ==================== GET AVAILABLE GRADES ====================

@router.get("/section-leaderboard/grades")
def get_available_grades(db: Session = Depends(get_db)):
    """Get list of grades that have exam attempts"""
    from app.models.exam_attempt_models import ExamAttemptModel
    from app.models.user_models import User
    
    grades = db.query(
        User.grade
    ).join(
        ExamAttemptModel, User.id == ExamAttemptModel.student_id
    ).distinct().filter(
        User.grade != None
    ).order_by(User.grade).all()
    
    return {
        "grades": [g[0] for g in grades if g[0] is not None]
    }


# ==================== GET SECTION CATEGORIES ====================

@router.get("/section-leaderboard/categories")
def get_section_categories(db: Session = Depends(get_db)):
    """Get list of unique section categories (sector names)"""
    from app.models import sector_models
    
    sectors = db.query(
        sector_models.SectorModel.name,
        sector_models.SectorModel.icon
    ).order_by(sector_models.SectorModel.name).all()
    
    return {
        "categories": [
            {"name": s[0], "icon": s[1]} 
            for s in sectors if s[0]
        ]
    }

@router.get("/student/{student_id}/global-recommendations")
def get_global_recommendations(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get global AI recommendation across all exams taken.
    """
    recommendation = analytics_crud.generate_global_recommendation(db, student_id)
    
    return {
        "student_id": student_id,
        "recommendation": recommendation
    }


# ==================== SCORE BY EXAM ====================

@router.get("/student/{student_id}/exam-scores")
def get_exam_scores(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get scores for each exam taken by the student.
    """
    exam_scores = analytics_crud.get_exam_wise_scores(db, student_id)
    
    return {
        "student_id": student_id,
        "exams_count": len(exam_scores),
        "exam_scores": exam_scores
    }


# ==================== ALL TOPICS PERFORMANCE TABLE ====================

@router.get("/student/{student_id}/topics-performance")
def get_topics_performance(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all topics performance table.
    """
    analytics_crud.calculate_all_analytics(db, student_id, force_refresh=False)
    performance_data = analytics_crud.get_all_topics_performance(db, student_id)
    
    return {
        "student_id": student_id,
        "topics_count": len(performance_data),
        "performance_table": performance_data
    }


# ==================== RECALCULATE ALL STUDENTS (ENHANCED) ====================

@router.post("/recalculate-all-enhanced")
def recalculate_all_students_enhanced(
    db: Session = Depends(get_db)
):
    """
    Enhanced recalculation for ALL students who have exam attempts.
    """
    result = analytics_crud.recalculate_all_students(db)
    return result


# ==================== MARKRROUTE FOR ADDITIONAL FEATURES ====================

@router.post("/recommendation/{recommendation_id}/mark-read")
def mark_recommendation_read(
    recommendation_id: int,
    db: Session = Depends(get_db)
):
    """Mark a recommendation as read"""
    recommendation = db.query(analytics_crud.AIRecommendation).filter(
        analytics_crud.AIRecommendation.id == recommendation_id
    ).first()
    
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )
    
    recommendation.is_read = 1
    db.commit()
    
    return {"success": True, "message": "Recommendation marked as read"}


@router.post("/recommendation/{recommendation_id}/mark-actioned")
def mark_recommendation_actioned(
    recommendation_id: int,
    db: Session = Depends(get_db)
):
    """Mark a recommendation as actioned (student took action)"""
    recommendation = db.query(analytics_crud.AIRecommendation).filter(
        analytics_crud.AIRecommendation.id == recommendation_id
    ).first()
    
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )
    
    recommendation.is_actioned = 1
    recommendation.is_read = 1
    db.commit()
    
    return {"success": True, "message": "Recommendation marked as actioned"}


# ==================== AVAILABLE EXAMS (NOT ATTEMPTED) ====================

@router.get("/student/{student_id}/available-exams")
def get_available_exams_for_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get available exams that the student has NOT attempted yet.
    Returns upcoming mock exams that the user can take.
    """
    from app.models.exam_models import ExamModel
    from app.models.sector_models import SectorModel
    from app.models.section_models import SectionModel
    from app.models.exam_attempt_models import ExamAttemptModel
    
    # Get all exams attempted by this student
    attempted_exam_ids = db.query(ExamAttemptModel.exam_id).filter(
        ExamAttemptModel.student_id == student_id,
        ExamAttemptModel.completed_at != None
    ).distinct().all()
    
    attempted_ids = [e[0] for e in attempted_exam_ids]
    
    # Get all available exams (not attempted)
    query = db.query(ExamModel)
    if attempted_ids:
        query = query.filter(~ExamModel.id.in_(attempted_ids))
    
    exams = query.all()
    
    result = []
    for exam in exams:
        # Get sector info
        sector = db.query(SectorModel).filter(SectorModel.id == exam.sector_id).first()
        
        # Get sections for this exam
        sections = db.query(SectionModel).filter(SectionModel.exam_id == exam.id).all()
        
        # Get first section name (if exists)
        section_name = sections[0].name if sections else "General"
        
        result.append({
            "id": exam.id,
            "exam_name": exam.name,
            "sector_id": exam.sector_id,
            "sector_name": sector.name if sector else "Unknown",
            "section_name": section_name,
            "total_questions": exam.total_questions or 0,
            "duration": exam.duration or 0,
            "total_marks": exam.total_marks or 0,
            "exam_type": exam.exam_type or "Mock",
            "pricing_type": exam.pricing_type or "Free",
            "amount": exam.amount or 0,
            "sections_count": len(sections)
        })
    
    return {
        "student_id": student_id,
        "total_available": len(result),
        "exams": result
    }


# ==================== AI RECOMMENDATION USING GROQ ====================

@router.get("/student/{student_id}/ai-recommendation")
def get_ai_recommendation(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get Groq AI recommendation based on average score.
    Analyzes different performance sectors and recommends Ethiopian 
    high school curriculum and entrance exam preparation.
    """
    import os
    import httpx
    from app.models import exam_models, section_models, question_models, sector_models
    from app.models.exam_attempt_models import ExamAttemptModel
    from app.models.student_answer_models import StudentAnswerModel
    from app.models.user_models import User
    
    # Get student info
    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Calculate analytics
    analytics_crud.calculate_all_analytics(db, student_id, force_refresh=False)
    
    # Get overall analytics
    overall = db.query(analytics_crud.StudentOverallAnalytics).filter(
        analytics_crud.StudentOverallAnalytics.student_id == student_id
    ).first()
    
    if not overall:
        return {
            "success": False,
            "message": "No analytics data available. Take some exams first!"
        }
    
    # Get subject-wise performance
    subjects = db.query(analytics_crud.StudentSubjectAnalytics).filter(
        analytics_crud.StudentSubjectAnalytics.student_id == student_id
    ).all()
    
    # Get topic-wise performance
    topics = db.query(analytics_crud.StudentTopicAnalytics).filter(
        analytics_crud.StudentTopicAnalytics.student_id == student_id
    ).order_by(analytics_crud.StudentTopicAnalytics.average_score).all()
    
    # Prepare performance data
    subject_performance = []
    for s in subjects:
        subject_performance.append({
            "subject": s.sector_name,
            "average_score": s.average_score,
            "exams_taken": s.total_exams_taken,
            "highest_score": s.highest_score,
            "lowest_score": s.lowest_score
        })
    
    # Find weak areas (below 60%)
    weak_areas = []
    for t in topics:
        if t.average_score < 60:
            weak_areas.append({
                "topic": t.section_name,
                "subject": t.sector_name,
                "score": t.average_score
            })
    
    # Find strong areas (70%+)
    strong_areas = []
    for t in topics:
        if t.average_score >= 70:
            strong_areas.append({
                "topic": t.section_name,
                "subject": t.sector_name,
                "score": t.average_score
            })
    
    average_score = overall.average_score
    total_exams = overall.total_exams_taken
    grade = student.grade or "Not set"
    
    # Ethiopian context prompt
    ethiopian_context = """You are an AI tutor specializing in Ethiopian high school education (Grade 9-12) and Ethiopian University Entrance Exam preparation. 
Your recommendations should be:
- Encouraging and supportive for students
- Progressive: start from easy concepts and gradually move to harder ones
- Aligned with Ethiopian national curriculum (Ethiopian General Education)
- Practical and actionable for Ethiopian University Entrance Exam (EUEE) success
- Include specific study tips for weak topics"""

    prompt = f"""{ethiopian_context}

Analyze this student's performance and provide personalized recommendations:

STUDENT INFO:
- Grade: {grade}
- Total exams taken: {total_exams}
- Overall average score: {average_score}%

SUBJECT PERFORMANCE:
{chr(10).join([f"- {s['subject']}: {s['average_score']}% (from {s['exams_taken']} exams)" for s in subject_performance])}

STRONG AREAS (70%+):
{chr(10).join([f"- {a['topic']} ({a['subject']}): {a['score']}%" for a in strong_areas[:5]]) if strong_areas else "- No strong areas yet"}

WEAK AREAS (below 60%):
{chr(10).join([f"- {a['topic']} ({a['subject']}): {a['score']}%" for a in weak_areas[:5]]) if weak_areas else "- No weak areas"}

Based on this analysis, provide a JSON response with:
1. "overall_analysis": Brief summary of student's learning journey (2-3 sentences)
2. "performance_highlights": List 2-3 subjects where student is performing well
3. "areas_needing_attention": List 2-3 weak topics with specific study recommendations
4. "ethiopian_exam_prep": Specific recommendations for Ethiopian University Entrance Exam preparation
5. "study_tips": 3-5 actionable study tips for the weak areas, ordered from easy to hard
6. "next_steps": Recommended actions for the next 2 weeks

Respond ONLY in JSON format with these exact keys.
"""
    
    # Call Groq API
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        # Return fallback recommendation
        return generate_fallback_ai_recommendation(average_score, weak_areas, strong_areas, total_exams)
    
    try:
        import json
        import re
        
        async def call_groq():
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-8b-instant",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                        "max_tokens": 1000
                    }
                )
                return response
        
        # Run async function
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(call_groq())
        loop.close()
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data["choices"][0]["message"]["content"]
            
            # Try to parse JSON
            json_match = re.search(r'\{[\s\S]*\}', ai_response)
            if json_match:
                try:
                    recommendation = json.loads(json_match.group())
                    return {
                        "success": True,
                        "student_id": student_id,
                        "average_score": average_score,
                        "total_exams": total_exams,
                        "grade": grade,
                        "recommendation": recommendation
                    }
                except json.JSONDecodeError:
                    pass
            
            # If JSON parsing fails, return fallback
            return generate_fallback_ai_recommendation(average_score, weak_areas, strong_areas, total_exams)
        else:
            return generate_fallback_ai_recommendation(average_score, weak_areas, strong_areas, total_exams)
            
    except Exception as e:
        print(f"AI Recommendation Error: {e}")
        return generate_fallback_ai_recommendation(average_score, weak_areas, strong_areas, total_exams)


def generate_fallback_ai_recommendation(average_score: float, weak_areas: list, strong_areas: list, total_exams: int) -> dict:
    """Generate fallback recommendation when AI is unavailable"""
    
    if average_score >= 80:
        assessment = "Excellent performance! You're mastering the material well."
        exam_prep = "Focus on advanced problems and timed practice tests to prepare for the Ethiopian University Entrance Exam."
        next_steps = "Take mock exams weekly, focus on time management, and review any mistakes carefully."
    elif average_score >= 60:
        assessment = "Good progress! You're building a solid foundation."
        exam_prep = "Continue practicing regularly. Focus on your weak areas to improve your entrance exam readiness."
        next_steps = "Dedicate 2 hours daily to weak topics, take one mock exam per week."
    elif average_score >= 40:
        assessment = "You're making progress but need more focus on fundamentals."
        exam_prep = "Start with basic concepts. The Ethiopian curriculum requires strong fundamentals."
        next_steps = "Review textbook basics for weak subjects, practice easy questions first, ask teachers for help."
    else:
        assessment = "Focus on building a strong foundation in core subjects."
        exam_prep = "Start from Grade 9 basics. The Ethiopian entrance exam tests comprehensive understanding."
        next_steps = "Create a study schedule, focus on one subject at a time, use online resources for extra practice."
    
    # Generate study tips from weak areas
    study_tips = []
    for area in weak_areas[:3]:
        study_tips.append(f"Practice more questions on {area['topic']} - start with easy problems and gradually increase difficulty")
    
    if not study_tips:
        study_tips = [
            "Continue practicing consistently across all subjects",
            "Review incorrect answers from previous exams",
            "Set aside time for regular revision"
        ]
    
    return {
        "success": True,
        "average_score": average_score,
        "total_exams": total_exams,
        "recommendation": {
            "overall_analysis": assessment,
            "performance_highlights": [a['topic'] for a in strong_areas[:3]] if strong_areas else ["Consistent learning"],
            "areas_needing_attention": [
                {
                    "topic": a['topic'],
                    "subject": a['subject'],
                    "score": a['score'],
                    "tip": f"Focus on {a['topic']} fundamentals and practice regularly"
                }
                for a in weak_areas[:3]
            ] if weak_areas else [{"topic": "All topics", "subject": "General", "tip": "Keep practicing!"}],
            "ethiopian_exam_prep": exam_prep,
            "study_tips": study_tips,
            "next_steps": next_steps
        },
        "note": "This is a basic recommendation. AI-powered detailed recommendations will be available soon."
    }
