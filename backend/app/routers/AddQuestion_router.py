from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
from datetime import datetime
from typing import Optional

from database import get_db
from app.models.AddQuestion_models import Question
from app.schemas.AddQuestion_schemas import QuestionCreate, QuestionUpdate

UPLOAD_DIR = Path("uploads/questions_pdfs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/questions", tags=["Questions"])

# ----- CREATE QUESTION (with FormData) -----
@router.post("/")
async def add_question(
    structure_id: int = Form(...),
    question_text: str = Form(...),
    option_a: str = Form(...),
    option_b: str = Form(...),
    option_c: str = Form(...),
    option_d: str = Form(...),
    correct_answer: str = Form(...),
    difficulty: str = Form(...),
    explanation: Optional[str] = Form(None),
    file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db)
):
    """
    Create a new question with optional PDF file upload
    Expects multipart/form-data
    """
    try:
        # Prepare question data
        question_data = {
            "structure_id": structure_id,
            "question_text": question_text,
            "option_a": option_a,
            "option_b": option_b,
            "option_c": option_c,
            "option_d": option_d,
            "correct_answer": correct_answer,
            "difficulty": difficulty,
            "explanation": explanation
        }
        
        # Save PDF if uploaded
        if file and file.filename:
            # Validate file type
            if not file.filename.lower().endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Only PDF files are allowed")
            
            # Generate unique filename
            timestamp = int(datetime.utcnow().timestamp())
            filename = f"{timestamp}_{file.filename}"
            file_path = UPLOAD_DIR / filename
            
            # Save file
            try:
                with file_path.open("wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                question_data["pdf_file"] = filename
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
            finally:
                await file.close()

        # Create question in database
        question = Question(**question_data)
        db.add(question)
        db.commit()
        db.refresh(question)
        
        return {
            "message": "Question saved successfully",
            "question_id": question.id,
            "has_pdf": question.pdf_file is not None
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ----- CREATE QUESTION (JSON only - alternative) -----
@router.post("/json")
def add_question_json(
    question: QuestionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new question without file upload (JSON only)
    """
    try:
        question_data = question.dict()
        db_question = Question(**question_data)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        return {
            "message": "Question saved successfully",
            "question_id": db_question.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ----- GET ALL QUESTIONS -----
@router.get("/")
def get_questions(db: Session = Depends(get_db)):
    """Get all questions with proper serialization"""
    try:
        questions = db.query(Question).all()
        # Convert to dict to avoid serialization issues
        return [
            {
                "id": q.id,
                "structure_id": q.structure_id,
                "question_text": q.question_text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "correct_answer": q.correct_answer,
                "difficulty": q.difficulty,
                "explanation": q.explanation,
                "pdf_file": q.pdf_file,
                "created_at": q.created_at.isoformat() if q.created_at else None
            }
            for q in questions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- UPDATE QUESTION (with FormData) -----
@router.put("/{question_id}")
async def update_question(
    question_id: int,
    structure_id: int = Form(...),
    question_text: str = Form(...),
    option_a: str = Form(...),
    option_b: str = Form(...),
    option_c: str = Form(...),
    option_d: str = Form(...),
    correct_answer: str = Form(...),
    difficulty: str = Form(...),
    explanation: Optional[str] = Form(None),
    file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db)
):
    """
    Update an existing question with optional PDF file upload
    """
    # Find the question
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    try:
        # Update fields
        question.structure_id = structure_id
        question.question_text = question_text
        question.option_a = option_a
        question.option_b = option_b
        question.option_c = option_c
        question.option_d = option_d
        question.correct_answer = correct_answer
        question.difficulty = difficulty
        question.explanation = explanation

        # Handle file upload if new file is provided
        if file and file.filename:
            # Validate file type
            if not file.filename.lower().endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Only PDF files are allowed")
            
            # Delete old PDF if exists
            if question.pdf_file:
                old_file = UPLOAD_DIR / question.pdf_file
                if old_file.exists():
                    old_file.unlink()
            
            # Save new PDF
            timestamp = int(datetime.utcnow().timestamp())
            filename = f"{timestamp}_{file.filename}"
            file_path = UPLOAD_DIR / filename
            
            try:
                with file_path.open("wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                question.pdf_file = filename
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
            finally:
                await file.close()

        db.commit()
        db.refresh(question)
        return {
            "message": "Question updated successfully",
            "question_id": question.id,
            "has_pdf": question.pdf_file is not None
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ----- UPDATE QUESTION (JSON only - alternative) -----
@router.put("/json/{question_id}")
def update_question_json(
    question_id: int,
    data: QuestionUpdate,
    db: Session = Depends(get_db)
):
    """
    Update question without file upload (JSON only)
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    try:
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(question, key, value)

        db.commit()
        db.refresh(question)
        return {
            "message": "Question updated successfully",
            "question_id": question.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ----- DELETE QUESTION -----
@router.delete("/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    """Delete a question and its associated PDF file"""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    try:
        # Delete associated PDF if exists
        if question.pdf_file:
            file_path = UPLOAD_DIR / question.pdf_file
            if file_path.exists():
                file_path.unlink()
        
        db.delete(question)
        db.commit()
        return {"message": "Question deleted successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ----- DOWNLOAD PDF -----
@router.get("/pdf/{question_id}")
def download_pdf(question_id: int, db: Session = Depends(get_db)):
    """Download PDF associated with a question"""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question or not question.pdf_file:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    file_path = UPLOAD_DIR / question.pdf_file
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File missing on server")
    
    return FileResponse(
        path=file_path, 
        filename=question.pdf_file,
        media_type='application/pdf'
    )

# ----- LIST ALL PDFs -----
@router.get("/pdfs")
def list_all_pdfs(db: Session = Depends(get_db)):
    """List all PDFs with their associated question info"""
    try:
        questions = db.query(Question).filter(Question.pdf_file.isnot(None)).all()
        pdfs = []
        for q in questions:
            file_path = UPLOAD_DIR / q.pdf_file
            pdfs.append({
                "id": q.id,
                "name": q.pdf_file,
                "size": file_path.stat().st_size if file_path.exists() else 0,
                "download_url": f"/questions/pdf/{q.id}",
                "question_id": q.id,
                "question_text": q.question_text[:50] + "..." if len(q.question_text) > 50 else q.question_text
            })
        return pdfs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- GET QUESTIONS BY STRUCTURE ID -----
@router.get("/by-structure/{structure_id}")
def get_questions_by_structure(structure_id: int, db: Session = Depends(get_db)):
    """Get all questions for a specific structure ID"""
    try:
        questions = db.query(Question).filter(Question.structure_id == structure_id).all()
        return [
            {
                "id": q.id,
                "structure_id": q.structure_id,
                "question_text": q.question_text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "correct_answer": q.correct_answer,
                "difficulty": q.difficulty,
                "explanation": q.explanation,
                "pdf_file": q.pdf_file,
                "created_at": q.created_at.isoformat() if q.created_at else None
            }
            for q in questions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))