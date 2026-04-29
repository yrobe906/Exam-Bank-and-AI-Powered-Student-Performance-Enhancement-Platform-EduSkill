from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from app.crud import practice_mock_crud
from app.schemas.practice_mock_schemas import (
    PracticeMockTestCreate,
    PracticeMockTestUpdate,
    PracticeMockTestResponse,
    PracticeMockTestWithQuestions,
    PracticeQuestionCreate,
    PracticeQuestionUpdate,
    PracticeQuestionResponse,
    PracticeAttemptCreate,
    PracticeAttemptResponse,
    PracticeTestSubmit,
)

router = APIRouter(
    prefix="/api/practice-mock",
    tags=["Practice Mock Tests"]
)


# ============== Practice Mock Test Endpoints ==============

@router.post("/tests", response_model=PracticeMockTestResponse)
def create_mock_test(test_data: PracticeMockTestCreate, db: Session = Depends(get_db)):
    """Create a new practice mock test"""
    return practice_mock_crud.create_practice_mock_test(db, test_data)


@router.get("/tests", response_model=List[PracticeMockTestResponse])
def get_mock_tests(
    skip: int = 0,
    limit: int = 100,
    subject: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all practice mock tests with optional filters"""
    return practice_mock_crud.get_practice_mock_tests(db, skip, limit, subject, is_active)


@router.get("/tests/subjects", response_model=List[str])
def get_subjects(db: Session = Depends(get_db)):
    """Get all unique subjects"""
    return practice_mock_crud.get_all_subjects(db)


@router.get("/tests/{test_id}", response_model=PracticeMockTestWithQuestions)
def get_mock_test(test_id: int, db: Session = Depends(get_db)):
    """Get a specific practice mock test with its questions"""
    test = practice_mock_crud.get_practice_mock_test(db, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Mock test not found")
    
    questions = practice_mock_crud.get_questions_by_test(db, test_id)
    
    test_dict = {
        "id": test.id,
        "title": test.title,
        "subject": test.subject,
        "description": test.description,
        "duration_minutes": test.duration_minutes,
        "is_active": test.is_active,
        "created_at": test.created_at,
        "updated_at": test.updated_at,
        "questions": questions
    }
    return test_dict


@router.patch("/tests/{test_id}", response_model=PracticeMockTestResponse)
def update_mock_test(test_id: int, test_data: PracticeMockTestUpdate, db: Session = Depends(get_db)):
    """Update a practice mock test"""
    test = practice_mock_crud.update_practice_mock_test(db, test_id, test_data)
    if not test:
        raise HTTPException(status_code=404, detail="Mock test not found")
    return test


@router.delete("/tests/{test_id}")
def delete_mock_test(test_id: int, db: Session = Depends(get_db)):
    """Delete a practice mock test and all its questions"""
    success = practice_mock_crud.delete_practice_mock_test(db, test_id)
    if not success:
        raise HTTPException(status_code=404, detail="Mock test not found")
    return {"message": "Mock test deleted successfully"}


# ============== Practice Question Endpoints ==============

@router.post("/questions", response_model=PracticeQuestionResponse)
def create_question(question_data: PracticeQuestionCreate, db: Session = Depends(get_db)):
    """Create a new practice question"""
    # Verify the mock test exists
    test = practice_mock_crud.get_practice_mock_test(db, question_data.mock_test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Mock test not found")
    
    return practice_mock_crud.create_practice_question(db, question_data)


@router.get("/tests/{test_id}/questions", response_model=List[PracticeQuestionResponse])
def get_test_questions(test_id: int, db: Session = Depends(get_db)):
    """Get all questions for a specific mock test"""
    test = practice_mock_crud.get_practice_mock_test(db, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Mock test not found")
    
    return practice_mock_crud.get_questions_by_test(db, test_id)


@router.get("/questions/{question_id}", response_model=PracticeQuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """Get a specific practice question"""
    question = practice_mock_crud.get_practice_question(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.patch("/questions/{question_id}", response_model=PracticeQuestionResponse)
def update_question(question_id: int, question_data: PracticeQuestionUpdate, db: Session = Depends(get_db)):
    """Update a practice question"""
    question = practice_mock_crud.update_practice_question(db, question_id, question_data)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.delete("/questions/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    """Delete a practice question"""
    success = practice_mock_crud.delete_practice_question(db, question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}


@router.get("/tests/{test_id}/questions-count")
def get_questions_count(test_id: int, db: Session = Depends(get_db)):
    """Get the count of questions for a test"""
    test = practice_mock_crud.get_practice_mock_test(db, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Mock test not found")
    
    count = practice_mock_crud.get_questions_count(db, test_id)
    return {"test_id": test_id, "questions_count": count}


@router.get("/subjects-with-counts")
def get_subjects_with_counts(db: Session = Depends(get_db)):
    """Get all subjects with their question counts"""
    return practice_mock_crud.get_subjects_with_counts(db)


# ============== Practice Mock Attempt Endpoints ==============

@router.post("/attempts", response_model=PracticeAttemptResponse)
def start_attempt(attempt_data: PracticeAttemptCreate, db: Session = Depends(get_db)):
    """Start a new practice mock test attempt"""
    # Verify the mock test exists
    test = practice_mock_crud.get_practice_mock_test(db, attempt_data.mock_test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Mock test not found")
    
    return practice_mock_crud.create_practice_attempt(db, attempt_data.student_id, attempt_data.mock_test_id)


@router.get("/attempts/{attempt_id}", response_model=PracticeAttemptResponse)
def get_attempt(attempt_id: int, db: Session = Depends(get_db)):
    """Get a specific practice attempt"""
    attempt = practice_mock_crud.get_practice_attempt(db, attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    return attempt


@router.get("/students/{student_id}/attempts", response_model=List[PracticeAttemptResponse])
def get_student_attempts(student_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """Get all attempts for a student"""
    return practice_mock_crud.get_student_attempts(db, student_id, skip, limit)


@router.get("/students/{student_id}/attempts/completed", response_model=List[PracticeAttemptResponse])
def get_student_completed_attempts(student_id: int, db: Session = Depends(get_db)):
    """Get all completed attempts for a student"""
    return practice_mock_crud.get_student_completed_attempts(db, student_id)


@router.post("/attempts/{attempt_id}/submit")
def submit_attempt(attempt_id: int, submit_data: PracticeTestSubmit, db: Session = Depends(get_db)):
    """Submit a practice mock test attempt with answers"""
    # Get the attempt
    attempt = practice_mock_crud.get_practice_attempt(db, attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    
    # Get the questions for this test
    questions = practice_mock_crud.get_questions_by_test(db, attempt.mock_test_id)
    if not questions:
        raise HTTPException(status_code=400, detail="No questions found for this test")
    
    # Create a map of question_id -> correct_answer
    question_answers = {q.id: q.correct_answer for q in questions}
    
    # Calculate score
    score = 0
    for answer in submit_data.answers:
        if answer.question_id in question_answers:
            if answer.selected_answer.lower() == question_answers[answer.question_id].lower():
                score += 1
    
    # Update the attempt
    updated_attempt = practice_mock_crud.update_practice_attempt(
        db, 
        attempt_id, 
        score=score,
        total_questions=len(questions),
        is_completed=True,
        time_taken_seconds=submit_data.time_taken_seconds
    )
    
    if not updated_attempt:
        raise HTTPException(status_code=500, detail="Failed to update attempt")
    
    return {
        "message": "Test submitted successfully",
        "attempt_id": attempt_id,
        "score": score,
        "total_questions": len(questions),
        "percentage": updated_attempt.percentage,
        "time_taken_seconds": submit_data.time_taken_seconds
    }
