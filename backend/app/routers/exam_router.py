# app/routers/exam_router.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from database import get_db
from app.models import sector_models, exam_models, section_models, question_models, test_models
from app.schemas import exam_schemas
import crud

# Remove prefix here since we'll add it in main.py
router = APIRouter(tags=["Exam Builder"])

# ============= SECTORS =============
@router.get("/sectors", response_model=List[exam_schemas.SectorOut])
async def get_sectors(db: Session = Depends(get_db)):
    """Get all sectors"""
    try:
        sectors = db.query(sector_models.SectorModel).all()
        return sectors
    except Exception as e:
        print(f"Error in /sectors: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============= EXAMS =============
@router.get("/exams", response_model=List[exam_schemas.ExamOut])
async def get_exams(
    sector_id: Optional[int] = Query(None, description="Filter by sector ID"),
    db: Session = Depends(get_db)
):
    """Get all exams, optionally filtered by sector"""
    try:
        query = db.query(exam_models.ExamModel)
        if sector_id:
            query = query.filter(exam_models.ExamModel.sector_id == sector_id)
        exams = query.all()
        return exams
    except Exception as e:
        print(f"Error in /exams: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============= CREATE EXAM =============
@router.post("/exams", response_model=exam_schemas.ExamOut)
async def create_exam(exam: exam_schemas.ExamBase, db: Session = Depends(get_db)):
    try:
        # Check if sector exists
        sector = db.query(sector_models.SectorModel).filter(
            sector_models.SectorModel.id == exam.sector_id
        ).first()
        
        if not sector:
            raise HTTPException(
                status_code=404, 
                detail=f"Sector with id {exam.sector_id} not found"
            )
        
        # Create new exam
        new_exam = exam_models.ExamModel(
            sector_id=exam.sector_id,
            name=exam.name,
            total_questions=exam.total_questions,
            duration=exam.duration,
            exam_type=exam.exam_type,
            total_marks=exam.total_marks,
            pricing_type=exam.pricing_type or "Free",
            amount=exam.amount or 0
        )
        
        db.add(new_exam)
        db.flush()  # Get the exam ID without committing
        
        # Create default section for the exam
        default_section = section_models.SectionModel(
            exam_id=new_exam.id,
            name="Section A",
            question_count=exam.total_questions,
            color="blue"
        )
        
        db.add(default_section)
        db.commit()
        db.refresh(new_exam)
        
        return new_exam
    except Exception as e:
        print(f"Error in /exams POST: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ============= SECTIONS =============
@router.get("/sections", response_model=List[exam_schemas.SectionOut])
async def get_sections(
    exam_id: Optional[int] = Query(None, description="Filter by exam ID"),
    db: Session = Depends(get_db)
):
    """Get sections, optionally filtered by exam"""
    try:
        query = db.query(section_models.SectionModel)
        if exam_id:
            query = query.filter(section_models.SectionModel.exam_id == exam_id)
        sections = query.all()
        return sections
    except Exception as e:
        print(f"Error in /sections: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Create a new section for an exam with custom name (like Biology Section, etc.)
@router.post("/create-section")
async def create_section_endpoint(
    request: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Create a new section for an exam with custom subject name"""
    try:
        exam_id = request.get("exam_id")
        name = request.get("name", "Section A")
        question_count = request.get("question_count", 0)
        color = request.get("color", "blue")
        
        if not exam_id:
            raise HTTPException(status_code=400, detail="exam_id is required")
        
        # Check if exam exists
        exam = db.query(exam_models.ExamModel).filter(
            exam_models.ExamModel.id == exam_id
        ).first()
        
        if not exam:
            raise HTTPException(
                status_code=404,
                detail=f"Exam with id {exam_id} not found"
            )
        
        # Create new section with custom name
        new_section = section_models.SectionModel(
            exam_id=exam_id,
            name=name,
            question_count=question_count,
            color=color
        )
        
        db.add(new_section)
        db.commit()
        db.refresh(new_section)
        
        return {
            "id": new_section.id,
            "exam_id": new_section.exam_id,
            "name": new_section.name,
            "question_count": new_section.question_count,
            "color": new_section.color,
            "message": "Section created successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in /create-section: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

# ... rest of your endpoints (keep them as they are) ...

# ============= QUESTIONS by Section =============
# app/routers/exam_router.py
@router.post("/question", response_model=Dict[str, Any])
async def create_question(question: exam_schemas.QuestionCreate, db: Session = Depends(get_db)):
    section = db.query(section_models.SectionModel).filter(
        section_models.SectionModel.id == question.section_id
    ).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    new_question = question_models.QuestionModel(
        section_id=question.section_id,
        question_text=question.question_text,
        option_a=question.option_a,
        option_b=question.option_b,
        option_c=question.option_c,
        option_d=question.option_d,
        correct_answer=question.correct_answer,
        difficulty=question.difficulty,
        marks=question.marks
    )
    
    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    # Update section's question count automatically
    section.question_count += 1
    db.commit()
    
    return {"id": new_question.id, "message": "Question added successfully"}

# ============= CREATE TEST (from test_models) =============
@router.post("/tests/draft", response_model=Dict[str, Any])
async def save_test_draft(
    test_data: exam_schemas.TestCreate,
    db: Session = Depends(get_db)
):
    """Save test as draft"""
    try:
        # Create new test - using TestModel if that's the class name
        # Check your test_models.py to see the actual class name
        new_test = test_models.TestModel(
            title=test_data.title,
            sector_id=test_data.sector_id,
            exam_id=test_data.exam_id,
            duration=test_data.duration,
            difficulty=test_data.difficulty,
            question_count=test_data.question_count,
            total_marks=getattr(test_data, 'total_marks', 0),
            exam_type=getattr(test_data, 'exam_type', ''),
            created_by=test_data.created_by or 1,
            is_draft=True
        )
        
        db.add(new_test)
        db.commit()
        db.refresh(new_test)
        
        return {"id": new_test.id, "message": "Test saved as draft"}
    except Exception as e:
        print(f"Error in /tests/draft: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tests", response_model=Dict[str, Any])
async def create_test(
    test_data: exam_schemas.TestCreate,
    db: Session = Depends(get_db)
):
    """Create and publish test"""
    try:
        # Create new published test
        new_test = test_models.TestModel(
            title=test_data.title,
            sector_id=test_data.sector_id,
            exam_id=test_data.exam_id,
            duration=test_data.duration,
            difficulty=test_data.difficulty,
            question_count=test_data.question_count,
            total_marks=getattr(test_data, 'total_marks', 0),
            exam_type=getattr(test_data, 'exam_type', ''),
            created_by=test_data.created_by or 1,
            is_draft=False
        )
        
        db.add(new_test)
        db.commit()
        db.refresh(new_test)
        
        return {"id": new_test.id, "message": "Test created successfully"}
    except Exception as e:
        print(f"Error in /tests: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ============= GET AVAILABLE EXAMS FOR STUDENTS =============
@router.get("/available-exams", response_model=List[Dict[str, Any]])
async def get_available_exams(
    sector_id: Optional[int] = Query(None, description="Filter by sector ID"),
    db: Session = Depends(get_db)
):
    """
    Get all available exams that students can take.
    Returns exams with their sector information.
    """
    try:
        query = db.query(exam_models.ExamModel)
        if sector_id:
            query = query.filter(exam_models.ExamModel.sector_id == sector_id)
        
        exams = query.all()
        
        # Get sector names for each exam
        result = []
        for exam in exams:
            sector = db.query(sector_models.SectorModel).filter(
                sector_models.SectorModel.id == exam.sector_id
            ).first()
            
            # Get section count
            sections = db.query(section_models.SectionModel).filter(
                section_models.SectionModel.exam_id == exam.id
            ).all()
            
            result.append({
                "id": exam.id,
                "name": exam.name,
                "sector_id": exam.sector_id,
                "sector_name": sector.name if sector else None,
                "total_questions": exam.total_questions,
                "duration": exam.duration,
                "total_marks": exam.total_marks,
                "exam_type": exam.exam_type,
                "pricing_type": exam.pricing_type or "Free",
                "amount": exam.amount or 0,
                "sections_count": len(sections)
            })
        
        return result
    except Exception as e:
        print(f"Error in /available-exams: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============= GET AVAILABLE TESTS FOR STUDENTS (Frontend Compatible) =============
@router.get("/student/available-tests", response_model=List[Dict[str, Any]])
async def get_student_available_tests(
    sector_id: Optional[int] = Query(None, description="Filter by sector ID"),
    db: Session = Depends(get_db)
):
    """
    Get all available tests for students in the format expected by the frontend.
    Returns tests with fields: id, title, authority, questions, time, marks, difficulty, category, is_published
    """
    try:
        query = db.query(exam_models.ExamModel)
        if sector_id:
            query = query.filter(exam_models.ExamModel.sector_id == sector_id)
        
        exams = query.all()
        
        result = []
        for exam in exams:
            # Get sector information
            sector = db.query(sector_models.SectorModel).filter(
                sector_models.SectorModel.id == exam.sector_id
            ).first()
            
            # Determine difficulty based on exam_type or use default
            difficulty = "Medium"
            if exam.exam_type:
                exam_type_lower = exam.exam_type.lower()
                if "hard" in exam_type_lower or "advanced" in exam_type_lower:
                    difficulty = "Hard"
                elif "easy" in exam_type_lower or "beginner" in exam_type_lower:
                    difficulty = "Easy"
            
            result.append({
                "id": exam.id,
                "title": exam.name,  # Map 'name' to 'title'
                "authority": sector.name if sector else "Unknown Authority",  # Map 'sector_name' to 'authority'
                "questions": exam.total_questions or 0,  # Map 'total_questions' to 'questions'
                "time": exam.duration or 0,  # Map 'duration' to 'time' (in minutes)
                "marks": exam.total_marks or 0,  # Map 'total_marks' to 'marks'
                "difficulty": difficulty,
                "category": sector.name if sector else "General",  # Use sector name as category
                "is_published": True,  # Always True for student-facing tests
                "pricing_type": exam.pricing_type or "Free",
                "amount": exam.amount or 0
            })
        
        return result
    except Exception as e:
        print(f"Error in /student/available-tests: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============= GET SINGLE TEST =============
@router.get("/tests/{test_id}", response_model=Dict[str, Any])
async def get_test(
    test_id: int,
    db: Session = Depends(get_db)
):
    """Get a single test by ID"""
    try:
        test = db.query(test_models.TestModel).filter(test_models.TestModel.id == test_id).first()
        if not test:
            raise HTTPException(status_code=404, detail="Test not found")
        return test
    except Exception as e:
        print(f"Error in /tests/{test_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============= HEALTH CHECK =============
@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "API is running"}
