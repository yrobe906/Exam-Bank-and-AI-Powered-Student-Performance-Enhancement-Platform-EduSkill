# Backend Exam CRUD Routes
# Add this to your FastAPI main.py or include it in your router

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel

from database import get_db
from app.models import exam_models

router = APIRouter(tags=["Exams"])

# Pydantic models for request/response
class ExamCreate(BaseModel):
    sector_id: int
    name: str
    total_questions: int
    duration: int
    exam_type: str
    total_marks: int
    difficulty: Optional[int] = 1

class ExamUpdate(BaseModel):
    name: Optional[str] = None
    total_questions: Optional[int] = None
    duration: Optional[int] = None
    exam_type: Optional[str] = None
    total_marks: Optional[int] = None
    difficulty: Optional[int] = None

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


# ================= CREATE EXAM =================
@router.post("/api/exams", response_model=ExamResponse, status_code=status.HTTP_201_CREATED)
def create_exam(exam: ExamCreate, db: Session = Depends(get_db)):
    """Create a new exam"""
    # Check if sector exists
    from app.models import sector_models
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
    db.commit()
    db.refresh(db_exam)
    
    return db_exam


# ================= GET EXAMS =================
@router.get("/api/exams", response_model=List[ExamResponse])
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


# ================= GET EXAM BY ID =================
@router.get("/api/exams/{exam_id}", response_model=ExamResponse)
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


# ================= UPDATE EXAM =================
@router.put("/api/exams/{exam_id}", response_model=ExamResponse)
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


# ================= DELETE EXAM =================
@router.delete("/api/exams/{exam_id}", status_code=status.HTTP_204_NO_CONTENT)
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
    
    # Delete related sections and questions first (cascade)
    from app.models import section_models, question_models
    
    # Get all sections for this exam
    sections = db.query(section_models.SectionModel).filter(
        section_models.SectionModel.exam_id == exam_id
    ).all()
    
    # Delete questions for each section
    for section in sections:
        db.query(question_models.QuestionModel).filter(
            question_models.QuestionModel.section_id == section.id
        ).delete()
    
    # Delete sections
    db.query(section_models.SectionModel).filter(
        section_models.SectionModel.exam_id == exam_id
    ).delete()
    
    # Delete exam
    db.delete(db_exam)
    db.commit()
    
    return None
