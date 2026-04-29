from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy import and_

from database import get_db
from app.models import exam_models, section_models, question_models, exam_attempt_models, student_answer_models
from app.services.gamification_service import get_gamification_service

router = APIRouter(tags=["Questions"])

# CREATE QUESTION ENDPOINT
@router.post("/questions")
def create_question(question: dict, db: Session = Depends(get_db)):
    try:
        section_id = question.get("section_id")
        question_text = question.get("question_text")
        option_a = question.get("option_a")
        option_b = question.get("option_b")
        option_c = question.get("option_c")
        option_d = question.get("option_d")
        correct_answer = question.get("correct_answer")
        difficulty_input = question.get("difficulty", 2)
        marks = question.get("marks", 1)
        
        if not section_id or not question_text or not correct_answer:
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Validate section_id exists in the database
        section = db.query(section_models.SectionModel).filter(
            section_models.SectionModel.id == section_id
        ).first()
        
        if not section:
            raise HTTPException(
                status_code=404, 
                detail=f"Section with id {section_id} not found. Please provide a valid section_id."
            )
        
        # Convert difficulty to integer if needed (database expects Integer)
        if isinstance(difficulty_input, str):
            difficulty_map = {"Easy": 1, "Medium": 2, "Hard": 3}
            difficulty = difficulty_map.get(difficulty_input, 2)
        else:
            difficulty = difficulty_input
        
        new_question = question_models.QuestionModel(
            section_id=section_id,
            question_text=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_answer=correct_answer,
            difficulty=difficulty,
            marks=marks
        )
        
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
        
        return {"id": new_question.id, "message": "Question created successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ================= GET QUESTIONS BY SECTION (for exam builder) =================
@router.get("/exam-questions")
def get_exam_questions(section_ids: str = None, db: Session = Depends(get_db)):
    """Get questions for exam builder, optionally filtered by section_ids (comma-separated)"""
    try:
        query = db.query(question_models.QuestionModel)
        
        if section_ids:
            section_id_list = [int(sid.strip()) for sid in section_ids.split(',')]
            query = query.filter(question_models.QuestionModel.section_id.in_(section_id_list))
        
        questions = query.all()
        
        return [
            {
                "id": q.id,
                "section_id": q.section_id,
                "question_text": q.question_text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "correct_answer": q.correct_answer,
                "difficulty": q.difficulty,
                "marks": q.marks
            }
            for q in questions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ================= UPDATE QUESTION =================
@router.put("/exam-questions/{question_id}")
def update_exam_question(question_id: int, question_data: dict, db: Session = Depends(get_db)):
    """Update a question for exam builder"""
    try:
        question = db.query(question_models.QuestionModel).filter(
            question_models.QuestionModel.id == question_id
        ).first()
        
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Update fields
        if "question_text" in question_data:
            question.question_text = question_data["question_text"]
        if "option_a" in question_data:
            question.option_a = question_data["option_a"]
        if "option_b" in question_data:
            question.option_b = question_data["option_b"]
        if "option_c" in question_data:
            question.option_c = question_data.get("option_c", "")
        if "option_d" in question_data:
            question.option_d = question_data.get("option_d", "")
        if "correct_answer" in question_data:
            question.correct_answer = question_data["correct_answer"]
        if "marks" in question_data:
            question.marks = question_data["marks"]
        if "difficulty" in question_data:
            difficulty_input = question_data["difficulty"]
            if isinstance(difficulty_input, str):
                difficulty_map = {"Easy": 1, "Medium": 2, "Hard": 3}
                question.difficulty = difficulty_map.get(difficulty_input, 2)
            else:
                question.difficulty = difficulty_input
        
        db.commit()
        db.refresh(question)
        
        return {"id": question.id, "message": "Question updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ================= DELETE QUESTION =================
@router.delete("/exam-questions/{question_id}")
def delete_exam_question(question_id: int, db: Session = Depends(get_db)):
    """Delete a question from exam builder"""
    try:
        question = db.query(question_models.QuestionModel).filter(
            question_models.QuestionModel.id == question_id
        ).first()
        
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        db.delete(question)
        db.commit()
        
        return {"message": "Question deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/student/available-tests")
def get_available_tests_for_student(db: Session = Depends(get_db)):
    """Get all published exams available for students"""
    from sqlalchemy import func
    
    # Get exams that have at least one question
    exams_with_questions = db.query(
        exam_models.ExamModel,
        func.count(question_models.QuestionModel.id).label('question_count')
    ).join(
        section_models.SectionModel,
        section_models.SectionModel.exam_id == exam_models.ExamModel.id
    ).join(
        question_models.QuestionModel,
        question_models.QuestionModel.section_id == section_models.SectionModel.id
    ).group_by(
        exam_models.ExamModel.id
    ).having(
        func.count(question_models.QuestionModel.id) > 0
    ).all()
    
    return {
        "exams": [
            {
                "id": exam.id,
                "title": exam.name,
                "difficulty": exam.difficulty or "Medium",
                "authority": exam.exam_type or "Unknown",
                "questions": question_count,
                "time": exam.duration,
                "marks": exam.total_marks,
                "category": str(exam.sector_id),
                "pricing_type": exam.pricing_type if hasattr(exam, 'pricing_type') else "Free",
                "amount": exam.amount if hasattr(exam, 'amount') else 0
            }
            for exam, question_count in exams_with_questions
        ]
    }

# ================= START EXAM ATTEMPT =================
@router.post("/exam/{exam_id}/start")
def start_exam_attempt(
    exam_id: int, 
    payload: Dict = None,
    db: Session = Depends(get_db)
):
    """
    Create a new exam attempt and return exam data WITHOUT correct answers
    (for student taking the exam)
    
    Supports difficulty filtering via payload.difficulty (1=Easy, 2=Medium, 3=Hard)
    or from exam's difficulty setting
    """
    # Get student_id from payload - this is required for multi-user support
    student_id = None
    difficulty_filter = None
    if payload and "student_id" in payload:
        student_id = payload.get("student_id")
    
    # Get difficulty filter from payload (for Test Configuration filtering)
    if payload and "difficulty" in payload:
        difficulty_filter = payload.get("difficulty")
    
    # If no student_id provided, try to get from localStorage on frontend or return error
    if not student_id:
        raise HTTPException(
            status_code=400, 
            detail="student_id is required. Please ensure you're logged in."
        )
    
    print(f"Starting exam with ID: {exam_id} for student: {student_id}, difficulty_filter: {difficulty_filter}")

    # Check if exam exists
    exam = db.query(exam_models.ExamModel).filter(
        exam_models.ExamModel.id == exam_id
    ).first()
    
    if not exam:
        raise HTTPException(status_code=404, detail=f"Exam with id {exam_id} not found")

# Import unlock check
    from app.crud.unlock_crud_fixed import student_has_exam_access

    # Check if user has unlock access first (bypass premium)
    if student_has_exam_access(db, student_id, exam_id):
        print(f"✅ User {student_id} has unlock access to exam {exam_id} - bypassing premium check")
    else:
        # Normal premium check
        pricing_type = getattr(exam, 'pricing_type', 'Free')
        exam_amount = getattr(exam, 'amount', 0)
        
        # Return pricing info so frontend can handle redirect
        if pricing_type == 'Premium' and exam_amount > 0:
            raise HTTPException(
                status_code=403,
                detail={
                    "message": "This is a premium exam",
                    "pricing_type": pricing_type,
                    "amount": exam_amount,
                    "require_subscription": True
                }
            )

    # Use exam's difficulty if no filter specified (default to Medium=2)
    difficulty_filter = difficulty_filter or 2

    # Check if student already completed this exam
    existing_completed_attempt = db.query(exam_attempt_models.ExamAttemptModel).filter(
        exam_attempt_models.ExamAttemptModel.student_id == student_id,
        exam_attempt_models.ExamAttemptModel.exam_id == exam_id,
        exam_attempt_models.ExamAttemptModel.completed_at != None
    ).first()

    if existing_completed_attempt:
        previous_score = existing_completed_attempt.score
        
        # Instead of raising an error, return the exam data with correct answers and user's previous answers
        return get_exam_data_for_review(
            existing_completed_attempt.id, 
            exam_id, 
            student_id, 
            db, 
            previous_score
        )

    # Check for existing incomplete attempt (allow resuming)
    existing_attempt = db.query(exam_attempt_models.ExamAttemptModel).filter(
        exam_attempt_models.ExamAttemptModel.student_id == student_id,
        exam_attempt_models.ExamAttemptModel.exam_id == exam_id,
        exam_attempt_models.ExamAttemptModel.completed_at == None
    ).first()

    if existing_attempt:
        print(f"Found existing incomplete attempt: {existing_attempt.id}")
        return get_exam_data_with_attempt(existing_attempt.id, exam_id, student_id, db, difficulty_filter)

    # Create new attempt
    new_attempt = exam_attempt_models.ExamAttemptModel(
        student_id=student_id,
        exam_id=exam_id,
        started_at=datetime.utcnow()
    )
    db.add(new_attempt)
    db.commit()
    db.refresh(new_attempt)
    
    print(f"Created new attempt: {new_attempt.id}")

    return get_exam_data_with_attempt(new_attempt.id, exam_id, student_id, db, difficulty_filter)


def get_exam_data_with_attempt(attempt_id: int, exam_id: int, student_id: int, db: Session, difficulty_filter: int = None):
    """Helper function to get exam data with attempt info (without correct answers)"""
    
    exam = db.query(exam_models.ExamModel).filter(
        exam_models.ExamModel.id == exam_id
    ).first()

    if not exam:
        raise HTTPException(status_code=404, detail=f"Exam with id {exam_id} not found")

    # Get sections for this exam
    sections = db.query(section_models.SectionModel).filter(
        section_models.SectionModel.exam_id == exam_id
    ).order_by(section_models.SectionModel.id).all()

    print(f"Found {len(sections)} sections for exam {exam_id}, difficulty_filter: {difficulty_filter}")

    result_sections = []
    for sec in sections:
        # Build query for questions - Get ALL questions without filtering by difficulty
        # FIX: The difficulty filter was causing questions to not show up if they didn't match
        question_query = db.query(question_models.QuestionModel).filter(
            question_models.QuestionModel.section_id == sec.id
        )
        
        # NOTE: If you want to filter by difficulty, uncomment the following block:
        # if difficulty_filter is not None:
        #     question_query = question_query.filter(
        #         question_models.QuestionModel.difficulty == difficulty_filter
        #     )
        
        questions = question_query.all()
        
        print(f"Section {sec.id} ({sec.name}) has {len(questions)} questions")
        
        # Debug: Log each question's difficulty
        for q in questions:
            print(f"  - Question {q.id}: difficulty={q.difficulty}, marks={q.marks}")

        # Get saved answers for this attempt
        saved_answers = db.query(student_answer_models.StudentAnswerModel).filter(
            student_answer_models.StudentAnswerModel.attempt_id == attempt_id
        ).all()
        
        # Create a map of question_id -> selected_answer
        answers_map = {ans.question_id: ans.selected_answer for ans in saved_answers if ans.selected_answer}

        sec_data = {
            "id": sec.id,
            "name": sec.name,
            "question_count": len(questions),
            "color": sec.color or "#2563eb",
            "questions": [
                {
                    "id": q.id,
                    "question_text": q.question_text,
                    "option_a": q.option_a,
                    "option_b": q.option_b,
                    "option_c": q.option_c,
                    "option_d": q.option_d,
                    "marks": q.marks or 1,
                    "difficulty": q.difficulty or "Medium",
                    "section_id": sec.id,
                    "section_name": sec.name,
                    "selected_answer": answers_map.get(q.id)
                }
                for q in questions
            ]
        }
        result_sections.append(sec_data)

    return {
        "attempt_id": attempt_id,
        "exam": {
            "id": exam.id,
            "name": exam.name,
            "sector_id": exam.sector_id,
            "total_questions": exam.total_questions,
            "duration": exam.duration,
            "total_marks": exam.total_marks,
            "exam_type": exam.exam_type,
            "pricing_type": getattr(exam, 'pricing_type', 'Free'),
            "amount": getattr(exam, 'amount', 0),
            "sections": result_sections
        }
    }


def get_exam_data_for_review(attempt_id: int, exam_id: int, student_id: int, db: Session, previous_score: int = 0):
    """Helper function to get exam data with correct answers and user answers for review (already taken exams)"""
    
    exam = db.query(exam_models.ExamModel).filter(
        exam_models.ExamModel.id == exam_id
    ).first()

    if not exam:
        raise HTTPException(status_code=404, detail=f"Exam with id {exam_id} not found")

    # Get sections for this exam
    sections = db.query(section_models.SectionModel).filter(
        section_models.SectionModel.exam_id == exam_id
    ).order_by(section_models.SectionModel.id).all()

    # Get user's answers for this attempt
    saved_answers = db.query(student_answer_models.StudentAnswerModel).filter(
        student_answer_models.StudentAnswerModel.attempt_id == attempt_id
    ).all()
    
    # Create maps for user answers and correctness
    user_answers_map = {ans.question_id: ans.selected_answer for ans in saved_answers if ans.selected_answer}
    is_correct_map = {ans.question_id: ans.is_correct for ans in saved_answers}

    result_sections = []
    for sec in sections:
        questions = db.query(question_models.QuestionModel).filter(
            question_models.QuestionModel.section_id == sec.id
        ).all()

        sec_data = {
            "id": sec.id,
            "name": sec.name,
            "question_count": len(questions),
            "color": sec.color or "#2563eb",
            "questions": [
                {
                    "id": q.id,
                    "question_text": q.question_text,
                    "option_a": q.option_a,
                    "option_b": q.option_b,
                    "option_c": q.option_c,
                    "option_d": q.option_d,
                    "correct_answer": q.correct_answer,
                    "marks": q.marks or 1,
                    "difficulty": q.difficulty or "Medium",
                    "section_id": sec.id,
                    "section_name": sec.name,
                    "selected_answer": user_answers_map.get(q.id),
                    "is_correct": is_correct_map.get(q.id, False)
                }
                for q in questions
            ]
        }
        result_sections.append(sec_data)

    return {
        "attempt_id": attempt_id,
        "already_taken": True,
        "previous_score": previous_score,
        "exam": {
            "id": exam.id,
            "name": exam.name,
            "sector_id": exam.sector_id,
            "total_questions": exam.total_questions,
            "duration": exam.duration,
            "total_marks": exam.total_marks,
            "exam_type": exam.exam_type,
            "pricing_type": getattr(exam, 'pricing_type', 'Free'),
            "amount": getattr(exam, 'amount', 0),
            "sections": result_sections
        }
    }


# ================= GET SAVED ANSWERS FOR ATTEMPT =================
@router.get("/attempt/{attempt_id}/answers")
def get_saved_answers(attempt_id: int, student_id: int = None, db: Session = Depends(get_db)):
    """Get all saved answers for an attempt"""
    if not student_id:
        raise HTTPException(status_code=400, detail="student_id is required")

    attempt = db.query(exam_attempt_models.ExamAttemptModel).filter(
        exam_attempt_models.ExamAttemptModel.id == attempt_id,
        exam_attempt_models.ExamAttemptModel.student_id == student_id
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    answers = db.query(student_answer_models.StudentAnswerModel).filter(
        student_answer_models.StudentAnswerModel.attempt_id == attempt_id
    ).all()

    # Return as a dictionary of question_id -> selected_answer
    answers_dict = {ans.question_id: ans.selected_answer for ans in answers if ans.selected_answer}

    return {"answers": answers_dict}


# ================= SAVE ANSWER =================
@router.post("/attempt/{attempt_id}/answer")
def save_answer(attempt_id: int, payload: Dict, db: Session = Depends(get_db)):
    """Save or update a student's answer for a question"""
    student_id = payload.get("student_id")
    if not student_id:
        raise HTTPException(status_code=400, detail="student_id is required in payload")
    
    question_id = payload.get("question_id")
    selected_option = payload.get("selected_option")

    # Validate input
    if not question_id:
        raise HTTPException(status_code=400, detail="question_id is required")
    
    if not selected_option:
        raise HTTPException(status_code=400, detail="selected_option is required")
    
    if selected_option not in ["A", "B", "C", "D"]:
        raise HTTPException(status_code=400, detail="selected_option must be A, B, C, or D")

    # Check if attempt exists and belongs to student
    attempt = db.query(exam_attempt_models.ExamAttemptModel).filter(
        exam_attempt_models.ExamAttemptModel.id == attempt_id,
        exam_attempt_models.ExamAttemptModel.student_id == student_id
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    if attempt.completed_at:
        raise HTTPException(status_code=400, detail="Exam already submitted")

    # Check if question exists
    question = db.query(question_models.QuestionModel).filter(
        question_models.QuestionModel.id == question_id
    ).first()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Verify question belongs to this exam
    section = db.query(section_models.SectionModel).filter(
        section_models.SectionModel.id == question.section_id
    ).first()
    
    if not section or section.exam_id != attempt.exam_id:
        raise HTTPException(status_code=400, detail="Question does not belong to this exam")

    # Check if answer already exists
    answer = db.query(student_answer_models.StudentAnswerModel).filter(
        student_answer_models.StudentAnswerModel.attempt_id == attempt_id,
        student_answer_models.StudentAnswerModel.question_id == question_id
    ).first()

    if answer:
        # Update existing answer
        answer.selected_answer = selected_option
        answer.is_correct = False
    else:
        # Create new answer
        answer = student_answer_models.StudentAnswerModel(
            attempt_id=attempt_id,
            question_id=question_id,
            selected_answer=selected_option,
            is_correct=False
        )
        db.add(answer)

    db.commit()
    
    return {
        "message": "Answer saved successfully",
        "question_id": question_id,
        "selected_option": selected_option
    }


# ================= CLEAR ANSWER =================
@router.delete("/attempt/{attempt_id}/answer/{question_id}")
def clear_answer(attempt_id: int, question_id: int, payload: Dict = None, db: Session = Depends(get_db)):
    """Clear a saved answer for a question"""
    student_id = None
    if payload and "student_id" in payload:
        student_id = payload.get("student_id")
    
    # If no student_id in payload, try to get from attempt
    if not student_id:
        attempt = db.query(exam_attempt_models.ExamAttemptModel).filter(
            exam_attempt_models.ExamAttemptModel.id == attempt_id
        ).first()
        if attempt:
            student_id = attempt.student_id
    
    if not student_id:
        raise HTTPException(status_code=400, detail="student_id is required")

    attempt = db.query(exam_attempt_models.ExamAttemptModel).filter(
        exam_attempt_models.ExamAttemptModel.id == attempt_id,
        exam_attempt_models.ExamAttemptModel.student_id == student_id
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    if attempt.completed_at:
        raise HTTPException(status_code=400, detail="Exam already submitted")

    answer = db.query(student_answer_models.StudentAnswerModel).filter(
        student_answer_models.StudentAnswerModel.attempt_id == attempt_id,
        student_answer_models.StudentAnswerModel.question_id == question_id
    ).first()

    if answer:
        db.delete(answer)
        db.commit()
        return {"message": "Answer cleared successfully"}
    
    return {"message": "No answer found to clear"}


# ================= SUBMIT EXAM =================
@router.post("/attempt/{attempt_id}/submit")
def submit_exam(attempt_id: int, payload: Dict = None, db: Session = Depends(get_db)):
    """Submit the exam and calculate score"""
    student_id = None
    if payload and "student_id" in payload:
        student_id = payload.get("student_id")
    
    # If no student_id in payload, try to get from attempt
    if not student_id:
        attempt = db.query(exam_attempt_models.ExamAttemptModel).filter(
            exam_attempt_models.ExamAttemptModel.id == attempt_id
        ).first()
        if attempt:
            student_id = attempt.student_id
    
    if not student_id:
        raise HTTPException(status_code=400, detail="student_id is required")
    
    print(f"Submit exam called for attempt_id: {attempt_id}, student_id: {student_id}")

    try:
        attempt = db.query(exam_attempt_models.ExamAttemptModel).filter(
            exam_attempt_models.ExamAttemptModel.id == attempt_id,
            exam_attempt_models.ExamAttemptModel.student_id == student_id
        ).first()

        if not attempt:
            print(f"Attempt {attempt_id} not found for student {student_id}")
            raise HTTPException(status_code=404, detail="Attempt not found")

        if attempt.completed_at:
            print(f"Attempt {attempt_id} already submitted at {attempt.completed_at}")
            raise HTTPException(status_code=400, detail="Exam already submitted")

        print(f"Found attempt {attempt_id} for exam {attempt.exam_id}")

        # Get all answers for this attempt
        answers = db.query(student_answer_models.StudentAnswerModel).filter(
            student_answer_models.StudentAnswerModel.attempt_id == attempt_id
        ).all()

        print(f"Found {len(answers)} answers for attempt {attempt_id}")

        # Get all sections for this exam to count total questions
        sections = db.query(section_models.SectionModel).filter(
            section_models.SectionModel.exam_id == attempt.exam_id
        ).all()
        
        total_questions_in_exam = 0
        for sec in sections:
            question_count = db.query(question_models.QuestionModel).filter(
                question_models.QuestionModel.section_id == sec.id
            ).count()
            total_questions_in_exam += question_count
        
        print(f"Total questions in exam: {total_questions_in_exam}")

        # Calculate score
        total_answered_marks = 0
        obtained_marks = 0
        correct_answers_count = 0
        total_answered_count = 0
        unanswered_count = 0
        
        # Create a set of question IDs that have been answered
        answered_question_ids = set()
        
        for ans in answers:
            if not ans.selected_answer:
                unanswered_count += 1
                continue
            
            answered_question_ids.add(ans.question_id)
            total_answered_count += 1
                
            question = db.query(question_models.QuestionModel).filter(
                question_models.QuestionModel.id == ans.question_id
            ).first()
            
            if not question:
                print(f"Question {ans.question_id} not found for answer {ans.id}")
                continue
                
            total_answered_marks += question.marks
            
            # Check if answer is correct
            student_answer = (ans.selected_answer or "").upper()
            correct_answer = (question.correct_answer or "").upper()
            is_correct = student_answer == correct_answer
            
            print(f"Q{question.id}: student={student_answer}, correct={correct_answer}, is_correct={is_correct}")
            
            if is_correct:
                obtained_marks += question.marks
                correct_answers_count += 1
                
            # Update answer with correctness info
            ans.is_correct = is_correct
        
        # Count unanswered questions as wrong
        unanswered_count = total_questions_in_exam - len(answered_question_ids)
        print(f"Unanswered questions (counted as wrong): {unanswered_count}")

        # Get total exam marks from exam model
        exam = db.query(exam_models.ExamModel).filter(
            exam_models.ExamModel.id == attempt.exam_id
        ).first()
        
        if not exam:
            print(f"Exam {attempt.exam_id} not found for attempt {attempt_id}")
            raise HTTPException(status_code=404, detail="Exam not found for this attempt")
        
        exam_total_marks = exam.total_marks or 0
        print(f"Exam total marks: {exam_total_marks}")
        
        # Update attempt
        attempt.score = obtained_marks
        attempt.completed_at = datetime.utcnow()
        
        print(f"Committing - score: {obtained_marks}, completed_at: {attempt.completed_at}")
        db.commit()
        print("Commit successful")

        # Calculate analytics after exam submission
        from app.crud import analytics_crud
        
        try:
            analytics_result = analytics_crud.calculate_all_analytics(db, student_id, force_refresh=True)
            print(f"Analytics calculated: {analytics_result}")
            
            # Calculate class rank
            class_rank = analytics_crud.calculate_class_rank(db, student_id)
            print(f"Class rank calculated: {class_rank}")
            
            # Update class rank in overall analytics
            overall = db.query(analytics_crud.StudentOverallAnalytics).filter(
                analytics_crud.StudentOverallAnalytics.student_id == student_id
            ).first()
            if overall:
                overall.class_rank = class_rank
                db.commit()
                
        except Exception as analytics_error:
            print(f"WARNING: Failed to calculate analytics: {str(analytics_error)}")

        percentage = (obtained_marks / exam_total_marks * 100) if exam_total_marks > 0 else 0
        print(f"Percentage: {percentage}")

        # Generate per-exam AI recommendation using DeepSeek AI
        ai_recommendation = None
        deepseek_recommendation = None
        try:
            from app.routers.ai_router import generate_deepseek_exam_recommendation
            import asyncio
            # Run the async function in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            deepseek_recommendation = loop.run_until_complete(
                generate_deepseek_exam_recommendation(db, student_id, attempt.exam_id)
            )
            loop.close()
            print(f"DeepSeek AI recommendation generated: {deepseek_recommendation.get('success')}")
        except Exception as ai_error:
            print(f"WARNING: Failed to generate DeepSeek AI recommendation: {str(ai_error)}")
            # Fallback to rule-based recommendation
            try:
                from app.crud import analytics_crud
                ai_recommendation = analytics_crud.generate_per_exam_recommendation(db, student_id, attempt_id)
                print(f"Fallback rule-based recommendation generated")
            except Exception as fallback_error:
                print(f"WARNING: Failed to generate fallback recommendation: {str(fallback_error)}")
        finally:
            # Use DeepSeek recommendation if available, otherwise use fallback
            if deepseek_recommendation:
                ai_recommendation = deepseek_recommendation.get('recommendation') or deepseek_recommendation

        # ==================== GAMIFICATION: Award XP ====================
        print(f"Starting gamification for student {student_id}, exam {attempt.exam_id}, percentage {percentage:.1f}%")
        xp_earned = 0
        xp_breakdown = {}
        
        try:
            gamification_service = get_gamification_service(db)
            
            # Award XP for exam submission (20 XP)
            print("Calling award_exam_submission_xp...")
            submission_xp = gamification_service.award_exam_submission_xp(student_id, attempt.exam_id)
            print(f"Submission XP result: {submission_xp}")
            if submission_xp is not None:
                xp_earned += submission_xp
                xp_breakdown['submission'] = submission_xp
            else:
                xp_breakdown['submission'] = 0
            
            # Award XP for exam result based on percentage
            print("Calling award_exam_result_xp...")
            result_xp = gamification_service.award_exam_result_xp(student_id, attempt.exam_id, percentage)
            print(f"Result XP result: {result_xp}")
            xp_earned += result_xp
            xp_breakdown['result'] = result_xp
            
            # Record activity for streak tracking
            gamification_service.record_activity(
                user_id=student_id,
                activity_type='exam_attempt',
                content_id=attempt.exam_id,
                content_type='exam'
            )
            print(f"Gamification COMPLETE: Total XP={xp_earned}, breakdown={xp_breakdown}")
            
        except Exception as gamification_error:
            print(f'ERROR in gamification: {str(gamification_error)}')
            import traceback
            traceback.print_exc()

        return {
            "attempt_id": attempt_id,
            "score": obtained_marks, 
            "total_marks": exam_total_marks, 
            "total_questions": total_questions_in_exam,
            "percentage": round(percentage, 2),
            "correct_count": correct_answers_count,
            "total_answered": total_answered_count,
            "unanswered_count": unanswered_count,
            "message": "Exam submitted successfully",
            "ai_recommendation": ai_recommendation,
            "xp_earned": xp_earned,
            "xp_breakdown": xp_breakdown
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in submit_exam: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ================= GET EXAM PREVIEW =================
@router.get("/exam/{exam_id}/preview")
def get_exam_preview(exam_id: int, db: Session = Depends(get_db)):
    """Get exam details with correct answers (for teachers/review)"""
    exam = db.query(exam_models.ExamModel).filter(
        exam_models.ExamModel.id == exam_id
    ).first()
    
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    sections = db.query(section_models.SectionModel).filter(
        section_models.SectionModel.exam_id == exam_id
    ).order_by(section_models.SectionModel.id).all()

    result_sections = []
    for sec in sections:
        questions = db.query(question_models.QuestionModel).filter(
            question_models.QuestionModel.section_id == sec.id
        ).all()

        sec_data = {
            "id": sec.id,
            "name": sec.name,
            "question_count": len(questions),
            "color": sec.color or "#2563eb",
            "questions": [
                {
                    "id": q.id,
                    "question_text": q.question_text,
                    "option_a": q.option_a,
                    "option_b": q.option_b,
                    "option_c": q.option_c,
                    "option_d": q.option_d,
                    "correct_answer": q.correct_answer,
                    "marks": q.marks,
                    "difficulty": q.difficulty
                }
                for q in questions
            ]
        }
        result_sections.append(sec_data)

    return {
        "id": exam.id,
        "name": exam.name,
        "sector_id": exam.sector_id,
        "total_questions": exam.total_questions,
        "duration": exam.duration,
        "total_marks": exam.total_marks,
        "exam_type": exam.exam_type,
        "pricing_type": getattr(exam, 'pricing_type', 'Free'),
        "amount": getattr(exam, 'amount', 0),
        "sections": result_sections
    }
