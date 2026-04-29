from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from models.student import Student
from auth import hash_password
from pathlib import Path

router = APIRouter(prefix="/students", tags=["Students"])

UPLOAD_DIR = Path("uploads/students")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/register")
async def register_student(
    full_name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    school_id: str = Form(...),
    grade: int = Form(...),
    gender: str = Form(...),
    profile_photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if db.query(Student).filter(Student.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(Student).filter(Student.username == username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Save uploaded photo
    ext = profile_photo.filename.split(".")[-1]
    file_name = f"{username}.{ext}"
    file_path = UPLOAD_DIR / file_name
    with open(file_path, "wb") as f:
        f.write(await profile_photo.read())

    student = Student(
        full_name=full_name,
        username=username,
        email=email,
        hashed_password=hash_password(password),
        school_id=school_id,
        grade=grade,
        gender=gender,
        profile_photo=str(file_path)
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return {"message": "Student registered successfully"}
