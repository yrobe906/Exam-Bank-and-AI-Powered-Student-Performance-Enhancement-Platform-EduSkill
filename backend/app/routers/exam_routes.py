from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel

from database import get_db
from app.models import exam_models, section_models, question_models, sector_models, exam_attempt_models
from app.models.analytics_models import StudentTopicAnalytics, StudentSubjectAnalytics

router = APIRouter(tags=["Exams"])

# ==================== PYDANTIC MODELS ====================

class ExamCreate(BaseModel):
    sector_id: int
    name: str
    total_questions: int
    duration: int
    exam_type: Optional[str] = "Unknown"
    total_marks: Optional[int] = 0
    difficulty: Optional[int] = 1

class ExamUpdate(BaseModel):
    name: Optional[str] = None
    total_questions: Optional[int] = None
    duration: Optional[int] = None
    exam_type: Optional[str] = None
    total_marks: Optional[int] = None
    difficulty: Optional[int] = None
    sector_id: Optional[int] = None


class ExamResponse(BaseModel):
    id: int
    sector_id: int
    name: str
    total_questions: int
    duration: int
    exam_type: str
    total_marks: int
    difficulty: Optional[int] = 1

    class Config:
        from_attributes = True

class SectionResponse(BaseModel):
    id: int
    exam_id: int
    name: str
    question_count: int
    color: Optional[str] = "blue"

    class Config:
        from_attributes = True

class QuestionResponse(BaseModel):
    id: int
    section_id: int
    section_name: Optional[str] = None
    question_text: str
    option_a: str
    option_b: str
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    correct_answer: str
    difficulty: int
    marks: int

    class Config:
        from_attributes = True


# ==================== EXAM CRUD OPERATIONS ====================

@router.post("/exams", response_model=ExamResponse, status_code=status.HTTP_201_CREATED)
def create_exam(exam: ExamCreate, db: Session = Depends(get_db)):
    """Create a new exam with a default section"""
    # Check if sector exists
    sector = db.query(sector_models.SectorModel).filter(
        sector_models.SectorModel.id == exam.sector_id
    ).first()
    
    if not sector:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sector with id {exam.sector_id} not found"
        )
    
    # Create new exam
    db_exam = exam_models.ExamModel(
        sector_id=exam.sector_id,
        name=exam.name,
        total_questions=exam.total_questions,
        duration=exam.duration,
        exam_type=exam.exam_type,
        total_marks=exam.total_marks,
        difficulty=exam.difficulty
    )
    
    db.add(db_exam)
    db.flush()  # Get the exam ID without committing
    
    # Create default section for the exam
    default_section = section_models.SectionModel(
        exam_id=db_exam.id,
        name="Section A",
        question_count=exam.total_questions,
        color="blue"
    )
    
    db.add(default_section)
    db.commit()
    db.refresh(db_exam)
    
    return db_exam


@router.get("/exams", response_model=List[ExamResponse])
def get_exams(
    sector_id: Optional[int] = None,
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all exams, optionally filtered by sector_id"""
    query = db.query(exam_models.ExamModel)
    
    if sector_id:
        query = query.filter(exam_models.ExamModel.sector_id == sector_id)
    
    exams = query.offset(skip).limit(limit).all()
    return exams


@router.get("/exams/{exam_id}", response_model=ExamResponse)
def get_exam(exam_id: int, db: Session = Depends(get_db)):
    """Get a specific exam by ID"""
    exam = db.query(exam_models.ExamModel).filter(
        exam_models.ExamModel.id == exam_id
    ).first()
    
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exam with id {exam_id} not found"
        )
    
    return exam


@router.put("/exams/{exam_id}", response_model=ExamResponse)
def update_exam(exam_id: int, exam_update: ExamUpdate, db: Session = Depends(get_db)):
    """Update an existing exam"""
    db_exam = db.query(exam_models.ExamModel).filter(
        exam_models.ExamModel.id == exam_id
    ).first()
    
    if not db_exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exam with id {exam_id} not found"
        )
    
    # Update only provided fields
    update_data = exam_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_exam, field, value)
    
    db.commit()
    db.refresh(db_exam)
    
    return db_exam


@router.delete("/exams/{exam_id}")
def delete_exam(exam_id: int, db: Session = Depends(get_db)):
    """Delete an exam"""
    db_exam = db.query(exam_models.ExamModel).filter(
        exam_models.ExamModel.id == exam_id
    ).first()
    
    if not db_exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exam with id {exam_id} not found"
        )
    
    # Get all sections for this exam
    sections = db.query(section_models.SectionModel).filter(
        section_models.SectionModel.exam_id == exam_id
    ).all()
    
    section_ids = [s.id for s in sections]
    sector_id = db_exam.sector_id
    
    # Delete related analytics records first (to avoid FK constraint violations)
    if section_ids:
        # Delete topic analytics referencing these sections
        db.query(StudentTopicAnalytics).filter(
            StudentTopicAnalytics.section_id.in_(section_ids)
        ).delete(synchronize_session=False)
    
    # Delete questions for each section
    for section in sections:
        db.query(question_models.QuestionModel).filter(
            question_models.QuestionModel.section_id == section.id
        ).delete(synchronize_session=False)
    
    # Delete exam attempts for this exam
    db.query(exam_attempt_models.ExamAttemptModel).filter(
        exam_attempt_models.ExamAttemptModel.exam_id == exam_id
    ).delete(synchronize_session=False)
    
    # Delete sections
    db.query(section_models.SectionModel).filter(
        section_models.SectionModel.exam_id == exam_id
    ).delete(synchronize_session=False)
    
    # Delete exam
    db.delete(db_exam)
    db.commit()
    
    return {"message": f"Exam with id {exam_id} deleted successfully", "deleted": True}



# ==================== SECTION OPERATIONS ====================

@router.get("/sections", response_model=List[SectionResponse])
def get_sections(
    exam_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get sections, optionally filtered by exam_id"""
    query = db.query(section_models.SectionModel)
    
    if exam_id:
        query = query.filter(section_models.SectionModel.exam_id == exam_id)
    
    sections = query.all()
    return sections


@router.post("/exams/{exam_id}/create-default-section")
def create_default_section(exam_id: int, db: Session = Depends(get_db)):
    """Create a default section for an exam that has no sections"""
    # Check if exam exists
    exam = db.query(exam_models.ExamModel).filter(
        exam_models.ExamModel.id == exam_id
    ).first()
    
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exam with id {exam_id} not found"
        )
    
    # Check if exam already has sections
    existing_sections = db.query(section_models.SectionModel).filter(
        section_models.SectionModel.exam_id == exam_id
    ).count()
    
    if existing_sections > 0:
        return {"message": "Exam already has sections", "count": existing_sections}
    
    # Create default section
    default_section = section_models.SectionModel(
        exam_id=exam_id,
        name="Section A",
        question_count=exam.total_questions,
        color="blue"
    )
    
    db.add(default_section)
    db.commit()
    
    return {"message": "Default section created successfully", "section_id": default_section.id}


# ==================== QUESTION OPERATIONS ====================

@router.get("/questions", response_model=List[QuestionResponse])
def get_questions_by_sections(
    section_ids: str = Query(None, description="Comma-separated section IDs"),
    db: Session = Depends(get_db)
):
    """
    Get questions by section IDs.
    Accepts comma-separated section IDs (e.g., "1,2,3") or single ID.
    Returns questions with all fields needed for the exam builder.
    """
    if not section_ids:
        return []
    
    # Parse section IDs from comma-separated string
    try:
        section_id_list = [int(sid.strip()) for sid in section_ids.split(',') if sid.strip()]
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid section IDs format. Use comma-separated integers (e.g., '1,2,3')"
        )
    
    if not section_id_list:
        return []
    
    # Get questions for the specified sections
    questions = db.query(question_models.QuestionModel).filter(
        question_models.QuestionModel.section_id.in_(section_id_list)
    ).all()
    
    # Get section info for each question
    result = []
    for q in questions:
        section = db.query(section_models.SectionModel).filter(
            section_models.SectionModel.id == q.section_id
        ).first()
        
        result.append({
            "id": q.id,
            "section_id": q.section_id,
            "section_name": section.name if section else None,
            "question_text": q.question_text,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d,
            "correct_answer": q.correct_answer,
            "difficulty": q.difficulty,
            "marks": q.marks
        })
    
    return result


# ==================== BULK OPERATIONS ====================

@router.post("/exams/bulk-create")
def bulk_create_exams(exams: List[ExamCreate], db: Session = Depends(get_db)):
    """Create multiple exams at once"""
    created_exams = []
    
    for exam_data in exams:
        # Check if sector exists
        sector = db.query(sector_models.SectorModel).filter(
            sector_models.SectorModel.id == exam_data.sector_id
        ).first()
        
        if not sector:
            continue  # Skip if sector doesn't exist
        
        # Create exam
        db_exam = exam_models.ExamModel(
            sector_id=exam_data.sector_id,
            name=exam_data.name,
            total_questions=exam_data.total_questions,
            duration=exam_data.duration,
            exam_type=exam_data.exam_type,
            total_marks=exam_data.total_marks,
            difficulty=exam_data.difficulty
        )
        
        db.add(db_exam)
        db.flush()
        
        # Create default section
        default_section = section_models.SectionModel(
            exam_id=db_exam.id,
            name="Section A",
            question_count=exam_data.total_questions,
            color="blue"
        )
        
        db.add(default_section)
        created_exams.append(db_exam)
    
    db.commit()
    
    return {"message": f"Successfully created {len(created_exams)} exams"}


@router.delete("/exams/bulk-delete")
def bulk_delete_exams(exam_ids: List[int], db: Session = Depends(get_db)):
    """Delete multiple exams at once"""
    deleted_count = 0
    
    for exam_id in exam_ids:
        db_exam = db.query(exam_models.ExamModel).filter(
            exam_models.ExamModel.id == exam_id
        ).first()
        
        if db_exam:
            # Delete related sections and questions
            sections = db.query(section_models.SectionModel).filter(
                section_models.SectionModel.exam_id == exam_id
            ).all()
            
            for section in sections:
                db.query(question_models.QuestionModel).filter(
                    question_models.QuestionModel.section_id == section.id
                ).delete()
            
            db.query(section_models.SectionModel).filter(
                section_models.SectionModel.exam_id == exam_id
            ).delete()
            
            db.delete(db_exam)
            deleted_count += 1
    
    db.commit()
    
    return {"message": f"Successfully deleted {deleted_count} exams"}
