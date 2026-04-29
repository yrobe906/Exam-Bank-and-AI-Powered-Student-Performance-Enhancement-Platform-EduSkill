from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.models.AddExam_models import ExamStructure
from app.schemas.AddExam_schemas import ExamStructureCreate

router = APIRouter(prefix="/api", tags=["Exam Structures"])

@router.post("/exam-structure")
def create_exam_structure(data: ExamStructureCreate, db: Session = Depends(get_db)):
    try:
        # Create exam structure instance
        exam = ExamStructure(
            exam_type=data.exam_type,
            year=data.year,
            university=data.university,
            model_type=data.model_type,
            subject=data.subject,
            topic=data.topic
        )
        db.add(exam)
        db.commit()
        db.refresh(exam)  # get generated ID

        return {"id": exam.id}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
