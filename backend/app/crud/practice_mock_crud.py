from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.practice_mock_models import PracticeMockTest, PracticeQuestion, PracticeMockAttempt
from app.schemas.practice_mock_schemas import (
    PracticeMockTestCreate,
    PracticeMockTestUpdate,
    PracticeQuestionCreate,
    PracticeQuestionUpdate,
)
from typing import List, Optional
from datetime import datetime


# ============== Practice Mock Test CRUD ==============

def create_practice_mock_test(db: Session, test_data: PracticeMockTestCreate) -> PracticeMockTest:
    """Create a new practice mock test"""
    db_test = PracticeMockTest(
        title=test_data.title,
        subject=test_data.subject,
        description=test_data.description,
        duration_minutes=test_data.duration_minutes,
        is_active=test_data.is_active,
    )
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test


def get_practice_mock_test(db: Session, test_id: int) -> Optional[PracticeMockTest]:
    """Get a practice mock test by ID"""
    return db.query(PracticeMockTest).filter(PracticeMockTest.id == test_id).first()


def get_practice_mock_tests(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    subject: Optional[str] = None,
    is_active: Optional[bool] = None
) -> List[PracticeMockTest]:
    """Get all practice mock tests with optional filters"""
    query = db.query(PracticeMockTest)
    
    if subject:
        query = query.filter(PracticeMockTest.subject == subject)
    if is_active is not None:
        query = query.filter(PracticeMockTest.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()


def get_all_subjects(db: Session) -> List[str]:
    """Get all unique subjects"""
    tests = db.query(PracticeMockTest.subject).distinct().all()
    return [test.subject for test in tests]


def update_practice_mock_test(
    db: Session, 
    test_id: int, 
    test_data: PracticeMockTestUpdate
) -> Optional[PracticeMockTest]:
    """Update a practice mock test"""
    db_test = db.query(PracticeMockTest).filter(PracticeMockTest.id == test_id).first()
    if not db_test:
        return None
    
    update_data = test_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_test, field, value)
    
    db.commit()
    db.refresh(db_test)
    return db_test


def delete_practice_mock_test(db: Session, test_id: int) -> bool:
    """Delete a practice mock test and its questions"""
    db_test = db.query(PracticeMockTest).filter(PracticeMockTest.id == test_id).first()
    if not db_test:
        return False
    
    db.delete(db_test)
    db.commit()
    return True


# ============== Practice Question CRUD ==============

def create_practice_question(db: Session, question_data: PracticeQuestionCreate) -> PracticeQuestion:
    """Create a new practice question"""
    db_question = PracticeQuestion(
        mock_test_id=question_data.mock_test_id,
        question_text=question_data.question_text,
        option_a=question_data.option_a,
        option_b=question_data.option_b,
        option_c=question_data.option_c,
        option_d=question_data.option_d,
        correct_answer=question_data.correct_answer,
        explanation=question_data.explanation,
        order_index=question_data.order_index,
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_practice_question(db: Session, question_id: int) -> Optional[PracticeQuestion]:
    """Get a practice question by ID"""
    return db.query(PracticeQuestion).filter(PracticeQuestion.id == question_id).first()


def get_questions_by_test(
    db: Session, 
    test_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[PracticeQuestion]:
    """Get all questions for a specific mock test"""
    return (
        db.query(PracticeQuestion)
        .filter(PracticeQuestion.mock_test_id == test_id)
        .order_by(PracticeQuestion.order_index)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_practice_question(
    db: Session, 
    question_id: int, 
    question_data: PracticeQuestionUpdate
) -> Optional[PracticeQuestion]:
    """Update a practice question"""
    db_question = db.query(PracticeQuestion).filter(PracticeQuestion.id == question_id).first()
    if not db_question:
        return None
    
    update_data = question_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_question, field, value)
    
    db.commit()
    db.refresh(db_question)
    return db_question


def delete_practice_question(db: Session, question_id: int) -> bool:
    """Delete a practice question"""
    db_question = db.query(PracticeQuestion).filter(PracticeQuestion.id == question_id).first()
    if not db_question:
        return False
    
    db.delete(db_question)
    db.commit()
    return True


def get_questions_count(db: Session, test_id: int) -> int:
    """Get the count of questions for a test"""
    return db.query(PracticeQuestion).filter(PracticeQuestion.mock_test_id == test_id).count()


def get_subjects_with_counts(db: Session):
    """Get all subjects with their question counts and exam counts"""
    results = (
        db.query(
            PracticeMockTest.subject,
            func.count(PracticeMockTest.id).label('exam_count'),
            func.coalesce(func.count(PracticeQuestion.id), 0).label('question_count')
        )
        .outerjoin(PracticeQuestion, PracticeMockTest.id == PracticeQuestion.mock_test_id)
        .filter(PracticeMockTest.is_active == True)
        .group_by(PracticeMockTest.subject)
        .all()
    )
    
    # Get sector mapping from sectors table
    from app.models.sector_models import SectorModel
    sectors = db.query(SectorModel).all()
    sector_map = {s.name: s.id for s in sectors}
    
    return [
        {
            "name": subject, 
            "question_count": count, 
            "exam_count": exam_count,
            "sector_id": sector_map.get(subject, None)
        }
        for subject, exam_count, count in results
    ]


# ============== Practice Mock Attempt CRUD ==============

def create_practice_attempt(db: Session, student_id: int, mock_test_id: int) -> PracticeMockAttempt:
    """Create a new practice mock test attempt"""
    db_attempt = PracticeMockAttempt(
        student_id=student_id,
        mock_test_id=mock_test_id,
        started_at=datetime.utcnow(),
    )
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)
    return db_attempt


def get_practice_attempt(db: Session, attempt_id: int) -> Optional[PracticeMockAttempt]:
    """Get a practice mock attempt by ID"""
    return db.query(PracticeMockAttempt).filter(PracticeMockAttempt.id == attempt_id).first()


def get_student_attempts(db: Session, student_id: int, skip: int = 0, limit: int = 50) -> List[PracticeMockAttempt]:
    """Get all attempts for a student"""
    return (
        db.query(PracticeMockAttempt)
        .filter(PracticeMockAttempt.student_id == student_id)
        .order_by(PracticeMockAttempt.started_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_student_completed_attempts(db: Session, student_id: int) -> List[PracticeMockAttempt]:
    """Get all completed attempts for a student"""
    return (
        db.query(PracticeMockAttempt)
        .filter(
            PracticeMockAttempt.student_id == student_id,
            PracticeMockAttempt.is_completed == True
        )
        .order_by(PracticeMockAttempt.completed_at.desc())
        .all()
    )


def update_practice_attempt(
    db: Session, 
    attempt_id: int, 
    score: int, 
    total_questions: int,
    is_completed: bool = True,
    time_taken_seconds: int = 0
) -> Optional[PracticeMockAttempt]:
    """Update a practice mock attempt with results"""
    db_attempt = db.query(PracticeMockAttempt).filter(PracticeMockAttempt.id == attempt_id).first()
    if not db_attempt:
        return None
    
    db_attempt.score = score
    db_attempt.total_questions = total_questions
    db_attempt.percentage = round((score / total_questions * 100), 2) if total_questions > 0 else 0.0
    db_attempt.is_completed = is_completed
    db_attempt.completed_at = datetime.utcnow() if is_completed else None
    db_attempt.time_taken_seconds = time_taken_seconds
    
    db.commit()
    db.refresh(db_attempt)
    return db_attempt


def delete_practice_attempt(db: Session, attempt_id: int) -> bool:
    """Delete a practice mock attempt"""
    db_attempt = db.query(PracticeMockAttempt).filter(PracticeMockAttempt.id == attempt_id).first()
    if not db_attempt:
        return False
    
    db.delete(db_attempt)
    db.commit()
    return True
