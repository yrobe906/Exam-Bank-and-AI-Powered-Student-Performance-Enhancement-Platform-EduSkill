from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
from pathlib import Path
import shutil
import os
from typing import Optional, List
from database import get_db
from app.models.downloadable_models_fixed import ModelExam, EntranceExam
from app.models.user_models import User
from auth import get_current_user  # Reuse existing auth

router = APIRouter(
    tags=["Downloadables"]
)

# Upload directory
DOWNLOADABLES_DIR = Path("uploads/downloadables")
DOWNLOADABLES_DIR.mkdir(parents=True, exist_ok=True)

# GET Model Exams (List with filters)
@router.get("/model-exams")
def get_model_exams(
    stream: Optional[str] = None,
    subject: Optional[str] = None,
    institution_type: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ModelExam).filter(ModelExam.is_active == True)
    
    if stream:
        query = query.filter(ModelExam.stream == stream)
    if subject:
        query = query.filter(ModelExam.subject == subject)
    if institution_type:
        query = query.filter(ModelExam.institution_type == institution_type)
    if search:
        query = query.filter(
            or_(
                ModelExam.title.contains(search),
                ModelExam.creator.contains(search)
            )
        )
    
    exams = query.all()
    return exams

# GET Entrance Exams (List with filters)
@router.get("/entrance-exams")
def get_entrance_exams(
    year: Optional[int] = None,
    stream: Optional[str] = None,
    subject: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(EntranceExam).filter(EntranceExam.is_active == True)
    
    if year:
        query = query.filter(EntranceExam.year == year)
    if stream:
        query = query.filter(EntranceExam.stream == stream)
    if subject:
        query = query.filter(EntranceExam.subject == subject)
    if search:
        query = query.filter(
            or_(
                EntranceExam.title.contains(search),
                EntranceExam.creator.contains(search)
            )
        )
    
    exams = query.all()
    return exams

# POST Model Exam (Create)
@router.post("/model-exams")
async def create_model_exam(
    title: str = Form(...),
    stream: str = Form(...),
    subject: str = Form(...),
    institution: str = Form(...),
    institution_type: Optional[str] = Form(None),
    creator: str = Form(...),
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate file
    allowed_types = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    if file.content_type not in allowed_types:
        raise HTTPException(400, "Only PDF, DOC, DOCX files allowed")
    
    # Save file
    file_path = DOWNLOADABLES_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    exam = ModelExam(
        title=title,
        stream=stream,
        subject=subject,
        institution=institution,
        institution_type=institution_type,
        creator=creator,
        file_path=str(file_path),
        file_name=file.filename,
        file_size=f"{file.size // 1024} KB" if file.size else "",
        file_type=file.content_type.split('/')[-1].upper(),
        description=description,
        uploaded_by=current_user.id
    )
    
    db.add(exam)
    db.commit()
    db.refresh(exam)
    
    return {"message": "Model exam created", "id": exam.id}

# POST Entrance Exam (Create)
@router.post("/entrance-exams")
async def create_entrance_exam(
    title: str = Form(...),
    year: int = Form(...),
    stream: str = Form(...),
    subject: str = Form(...),
    institution: str = Form(...),
    creator: str = Form(...),
    file: UploadFile = File(...),
    question_count: Optional[int] = Form(None),
    time_limit: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate file
    allowed_types = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    if file.content_type not in allowed_types:
        raise HTTPException(400, "Only PDF, DOC, DOCX files allowed")
    
    # Save file
    file_path = DOWNLOADABLES_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    exam = EntranceExam(
        title=title,
        year=year,
        stream=stream,
        subject=subject,
        institution=institution,
        creator=creator,
        file_path=str(file_path),
        file_name=file.filename,
        file_size=f"{file.size // 1024} KB" if file.size else "",
        file_type=file.content_type.split('/')[-1].upper(),
        question_count=question_count,
        time_limit=time_limit,
        uploaded_by=current_user.id
    )
    
    db.add(exam)
    db.commit()
    db.refresh(exam)
    
    return {"message": "Entrance exam created", "id": exam.id}

# PUT Model Exam (Update)
@router.put("/model-exams/{exam_id}")
async def update_model_exam(
    exam_id: int,
    title: Optional[str] = Form(None),
    stream: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    institution: Optional[str] = Form(None),
    institution_type: Optional[str] = Form(None),
    creator: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exam = db.query(ModelExam).filter(ModelExam.id == exam_id, ModelExam.is_active == True).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Model exam not found")
    
    # Update fields
    if title:
        exam.title = title
    if stream:
        exam.stream = stream
    if subject:
        exam.subject = subject
    if institution:
        exam.institution = institution
    if institution_type:
        exam.institution_type = institution_type
    if creator:
        exam.creator = creator
    if description:
        exam.description = description
    
    if file:
        allowed_types = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        if file.content_type not in allowed_types:
            raise HTTPException(400, "Only PDF, DOC, DOCX files allowed")
        file_path = DOWNLOADABLES_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        exam.file_path = str(file_path)
        exam.file_name = file.filename
        exam.file_size = f"{file.size // 1024} KB"
        exam.file_type = file.content_type.split('/')[-1].upper()
    
    db.commit()
    db.refresh(exam)
    return {"message": "Model exam updated"}

# PUT Entrance Exam (Update)
@router.put("/entrance-exams/{exam_id}")
async def update_entrance_exam(
    exam_id: int,
    title: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    stream: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    institution: Optional[str] = Form(None),
    creator: Optional[str] = Form(None),
    question_count: Optional[int] = Form(None),
    time_limit: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exam = db.query(EntranceExam).filter(EntranceExam.id == exam_id, EntranceExam.is_active == True).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Entrance exam not found")
    
    if title:
        exam.title = title
    if year:
        exam.year = year
    if stream:
        exam.stream = stream
    if subject:
        exam.subject = subject
    if institution:
        exam.institution = institution
    if creator:
        exam.creator = creator
    if question_count:
        exam.question_count = question_count
    if time_limit:
        exam.time_limit = time_limit
    
    if file:
        allowed_types = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        if file.content_type not in allowed_types:
            raise HTTPException(400, "Only PDF, DOC, DOCX files allowed")
        file_path = DOWNLOADABLES_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        exam.file_path = str(file_path)
        exam.file_name = file.filename
        exam.file_size = f"{file.size // 1024} KB"
    
    db.commit()
    db.refresh(exam)
    return {"message": "Entrance exam updated"}

# DELETE Model Exam
@router.delete("/model-exams/{exam_id}")
def delete_model_exam(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exam = db.query(ModelExam).filter(ModelExam.id == exam_id, ModelExam.is_active == True).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Model exam not found")
    exam.is_active = False
    db.commit()
    return {"message": "Model exam soft deleted"}

# DELETE Entrance Exam
@router.delete("/entrance-exams/{exam_id}")
def delete_entrance_exam(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exam = db.query(EntranceExam).filter(EntranceExam.id == exam_id, EntranceExam.is_active == True).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Entrance exam not found")
    exam.is_active = False
    db.commit()
    return {"message": "Entrance exam soft deleted"}

# Download Model Exam file
@router.get("/model-exams/{exam_id}/download")
def download_model_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(ModelExam).filter(ModelExam.id == exam_id, ModelExam.is_active == True).first()
    if not exam or not os.path.exists(exam.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Increment download count
    exam.download_count += 1
    db.commit()
    
    def file_iterator(file_path, chunk_size=8192):
        with open(file_path, 'rb') as file:
            while chunk := file.read(chunk_size):
                yield chunk
    
    return StreamingResponse(
        file_iterator(exam.file_path),
        media_type=f"application/{exam.file_type.lower()}",
        headers={"Content-Disposition": f"attachment; filename={exam.file_name}"}
    )

# Download Entrance Exam file
@router.get("/entrance-exams/{exam_id}/download")
def download_entrance_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(EntranceExam).filter(EntranceExam.id == exam_id, EntranceExam.is_active == True).first()
    if not exam or not os.path.exists(exam.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Increment download count
    exam.download_count += 1
    db.commit()
    
    def file_iterator(file_path, chunk_size=8192):
        with open(file_path, 'rb') as file:
            while chunk := file.read(chunk_size):
                yield chunk
    
    return StreamingResponse(
        file_iterator(exam.file_path),
        media_type=f"application/{exam.file_type.lower()}",
        headers={"Content-Disposition": f"attachment; filename={exam.file_name}"}
    )
