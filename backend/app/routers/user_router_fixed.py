from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import secrets
import shutil
from pathlib import Path
from jose import jwt
import os

from app.models.user_models import User
from app.utils.hashing import hash_password, verify_password
from app.schemas.user_edit_schemas import UserEditRequest
from app.crud.user_crud import get_user_by_id, update_user, can_edit_user
from database import get_db
from app.auth import get_current_user
from sqlalchemy import func
from app.models import ExamAttemptModel
from app.models.analytics_models import StudentOverallAnalytics
from app.models.resource_models import Resource

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"

router = APIRouter(tags=["Users"])

UPLOAD_DIR = Path("uploads/users")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def normalize_profile_photo_value(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    # Normalize path separators and remove leading slashes
    value = value.replace('\\', '/').lstrip('/')
    # Remove all leading 'uploads/' prefixes
    while value.startswith("uploads/"):
        value = value[len("uploads/"):]
    return value


def get_profile_photo_url(value: Optional[str]) -> Optional[str]:
    normalized = normalize_profile_photo_value(value)
    return normalized


@router.post("/register")
async def register_user(
    full_name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    gender: str = Form(...),
    school_id: str = Form(None),
    grade: Optional[int] = Form(None),
    phone: str = Form(None),
    school_name: str = Form(None),
    subject_assigned: str = Form(None),
    teaching_grade: Optional[int] = Form(None),
    woreda: str = Form(None),
    school_supervising: str = Form(None),
    profile_photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if db.query(User).filter((User.email == email) | (User.username == username)).first():
        raise HTTPException(status_code=400, detail="Email or Username already exists")

    ext = profile_photo.filename.split(".")[-1]
    photo_filename = f"{username}_{int(datetime.utcnow().timestamp())}.{ext}"
    photo_path = UPLOAD_DIR / photo_filename
    with open(photo_path, "wb") as buffer:
        shutil.copyfileobj(profile_photo.file, buffer)

    user = User(
        full_name=full_name.strip(),
        username=username.strip(),
        email=email.lower().strip(),
        password_hash=hash_password(password),
        role=role,
        gender=gender.lower(),
        school_id=school_id,
        grade=grade,
        phone=phone,
        school_name=school_name,
        subject_assigned=subject_assigned,
        teaching_grade=teaching_grade,
        woreda=woreda,
        school_supervising=school_supervising,
        profile_photo=f"users/{photo_filename}",
        status="pending",
        created_at=datetime.utcnow()
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Registration submitted. Waiting for admin approval."}

@router.get("/status/{username}")
def check_status(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": user.status}

@router.post("/login")
def login_user(
    username_or_email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info(f"Login attempt for: {username_or_email}")
    
    user = db.query(User).filter(
        (User.username == username_or_email) | 
        (User.email == username_or_email.lower())
    ).first()
    
    logger.info(f"User found: {user.username if user else 'None'}, status: {user.status if user else 'N/A'}")

    if not user:
        logger.warning(f"No user found for {username_or_email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    logger.info(f"Hash format: {user.password_hash[:10]}..., length: {len(user.password_hash) if user.password_hash else 0}")
    
    password_match = verify_password(password, user.password_hash)
    logger.info(f"PBKDF2 verify result: {password_match}")
    
    if not password_match:
        logger.warning(f"Password mismatch for user {user.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.status == "pending":
        logger.info(f"User {user.username} pending approval")
        return {
            "status": "pending",
            "username": user.username,
            "message": "Your account is pending approval"
        }

    if user.status == "rejected":
        logger.info(f"User {user.username} rejected")
        return {
            "status": "rejected",
            "username": user.username,
            "message": "Your account was rejected"
        }

    logger.info(f"Generating token for user {user.username} ({user.role})")
    
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role
    }
    
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    logger.info(f"Login successful for {user.username}")
    
    return {
        "message": "Login successful",
        "token": access_token,
        "role": user.role,
        "username": user.username,
        "user_id": user.id,
        "full_name": user.full_name,
        "school_id": user.school_id,
        "profile_photo": get_profile_photo_url(user.profile_photo),
        "email": getattr(user, 'email', None),
        "phone": getattr(user, 'phone', None),
        "grade": getattr(user, 'grade', None),
        "subject_assigned": getattr(user, 'subject_assigned', None)
    }

@router.get("/profile")
def get_current_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current logged-in user's profile"""
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "username": current_user.username,
        "role": current_user.role,
        "profile_photo": get_profile_photo_url(current_user.profile_photo),
        "email": getattr(current_user, 'email', None),
        "phone": getattr(current_user, 'phone', None),
        "grade": getattr(current_user, 'grade', None),
        "subject_assigned": getattr(current_user, 'subject_assigned', None),
        "school_id": getattr(current_user, 'school_id', None),
        "school_name": getattr(current_user, 'school_name', None),
        "teaching_grade": getattr(current_user, 'teaching_grade', None),
        "status": current_user.status
    }

@router.get("/profile/{username}")
def get_user_profile(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "full_name": user.full_name,
        "username": user.username,
        "profile_photo": get_profile_photo_url(user.profile_photo),
        "grade": user.grade,             
        "school_id": user.school_id,     
        "subject_assigned": user.subject_assigned,
        "teaching_grade": user.teaching_grade,
        "school_name": user.school_name,
        "role": user.role
    }

@router.get("/summary")
def get_user_summary(db: Session = Depends(get_db)):
    all_roles = ["student", "teacher", "eduoffice"]
    total_users = db.query(func.count(User.id)).filter(User.role.in_(all_roles)).scalar() or 0
    active_users = db.query(func.count(User.id)).filter(
        User.role.in_(all_roles),
        User.status.notin_(["pending", "rejected"])
    ).scalar() or 0
    return {
        "totalUsers": total_users,
        "activeUsers": active_users
    }

@router.get("/teacher/student-performance")
def get_teacher_student_performance(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["teacher", "eduoffice"]:
        raise HTTPException(status_code=403, detail="Access denied: Teacher or EduOffice only")
    
    # Find students
    query = db.query(User).filter(User.role == "student")
    
    if current_user.role == "teacher":
        # Filter by teacher's grade
        query = query.filter(User.grade == current_user.teaching_grade)
    
    students = query.offset(offset).limit(limit).all()
    
    performance_data = []
    total_avg = 0
    for student in students:
        # Get analytics data
        analytics = db.query(StudentOverallAnalytics).filter(
            StudentOverallAnalytics.student_id == student.id
        ).first()
        
        if analytics:
            avg_score = analytics.average_score
            total_exams = analytics.total_exams_taken
        else:
            avg_score = 0.0
            total_exams = 0
        
        total_avg += avg_score
        
        # Recent exam scores (last 3) - still from exam_attempts for details
        recent_attempts = db.query(ExamAttemptModel).filter(
            ExamAttemptModel.student_id == student.id
        ).order_by(
            ExamAttemptModel.completed_at.desc()
        ).limit(3).all()
        recent_scores = [{"exam_id": a.exam_id, "score": a.score, "date": str(a.completed_at) if a.completed_at else None} for a in recent_attempts]
        
        # Determine status based on avg_score
        if avg_score >= 80:
            status = "Excellent"
        elif avg_score >= 60:
            status = "Good"
        else:
            status = "Needs Work"
        
        performance_data.append({
            "student_id": student.id,
            "username": student.username,
            "full_name": student.full_name,
            "grade": student.grade,
            "profile_photo": get_profile_photo_url(student.profile_photo),
            "xp_points": getattr(student, 'xp_points', 0),
            "average_score": round(avg_score, 2),
            "total_exams_taken": total_exams,
            "recent_scores": recent_scores
        })
    
    # Sort students by average_score descending for ranking
    sorted_students = sorted(performance_data, key=lambda x: x['average_score'], reverse=True)
    
    # Assign ranks
    for i, student in enumerate(sorted_students, 1):
        student['rank'] = i
    
    return {
        "students": sorted_students,
        "total": len(students),
        "limit": limit,
        "offset": offset
    }

@router.get("/teacher/dashboard-stats")
def get_teacher_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Access denied: Teacher only")

    students = db.query(User).filter(User.role == "student", User.grade == current_user.teaching_grade).all()
    total_students = len(students)
    active_students = 0
    total_score = 0.0

    for student in students:
        analytics = db.query(StudentOverallAnalytics).filter(StudentOverallAnalytics.student_id == student.id).first()
        score = analytics.average_score if analytics else 0.0
        if score > 50:
            active_students += 1
        total_score += score

    avg_readiness = round((total_score / total_students) if total_students else 0.0, 2)

    return {
        "totalStudents": total_students,
        "activeThisWeek": active_students,
        "avgReadiness": avg_readiness
    }

@router.get("/teacher/resources")
def get_teacher_resources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Access denied: Teacher only")

    resources = db.query(Resource).filter(Resource.is_active == True).all()
    counts = {"notes": 0, "slides": 0, "videos": 0, "books": 0}

    for resource in resources:
        resource_type = (resource.type or "").strip().lower()
        if resource_type in ["note", "notes"]:
            counts["notes"] += 1
        elif resource_type in ["slide", "slides"]:
            counts["slides"] += 1
        elif resource_type in ["video", "videos"]:
            counts["videos"] += 1
        elif resource_type in ["book", "books"]:
            counts["books"] += 1

    return counts

@router.get("/teacher/recent-uploads")
def get_teacher_recent_uploads(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Access denied: Teacher only")

    recent_resources = db.query(Resource).filter(
        Resource.is_active == True
    ).order_by(Resource.created_at.desc()).limit(3).all()

    return [
        {
            "id": resource.id,
            "title": resource.title,
            "type": resource.type,
            "file_path": resource.file_path,
            "file_name": resource.file_name,
            "created_at": resource.created_at.isoformat() if resource.created_at else None
        }
        for resource in recent_resources
    ]

@router.put("/profile")
def update_user_profile(
    full_name: Optional[str] = Form(None),
    username: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    grade: Optional[int] = Form(None),
    subject_assigned: Optional[str] = Form(None),
    school_id: Optional[str] = Form(None),
    current_password: Optional[str] = Form(None),
    new_password: Optional[str] = Form(None),
    profile_photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.crud.user_crud import update_user
    from app.utils.hashing import verify_password, hash_password

    update_data = {}
    
    if full_name:
        update_data['full_name'] = full_name.strip()
    if username:
        update_data['username'] = username.strip()
    if school_id:
        update_data['school_id'] = school_id
    if grade is not None:
        update_data['grade'] = grade
    if phone:
        update_data['phone'] = phone
    if subject_assigned:
        update_data['subject_assigned'] = subject_assigned
    if email:
        update_data['email'] = email

    if profile_photo and profile_photo.filename:
        UPLOAD_DIR = Path("uploads/users")
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        ext = profile_photo.filename.split('.')[-1]
        photo_filename = f"{current_user.username}_{int(datetime.utcnow().timestamp())}.{ext}"
        photo_path = UPLOAD_DIR / photo_filename
        with open(photo_path, "wb") as f:
            shutil.copyfileobj(profile_photo.file, f)
        update_data['profile_photo'] = f"users/{photo_filename}"
    
    if new_password:
        if not current_password:
            raise HTTPException(status_code=400, detail="Current password required")
        if not verify_password(current_password, current_user.password_hash):
            raise HTTPException(status_code=400, detail="Current password incorrect")
        update_data['password_hash'] = hash_password(new_password)

    try:
        updated_user = update_user(db, current_user, update_data, current_user.role)
    except Exception as e:
        db.rollback()
        # Check for specific database errors
        if "unique constraint" in str(e).lower() or "duplicate key" in str(e).lower():
            raise HTTPException(status_code=400, detail="Username or email already exists")
        raise HTTPException(status_code=500, detail="Update failed. Please try again.")
    
    return {
        "message": "Profile updated successfully",
        "user": {
            "id": updated_user.id,
            "full_name": updated_user.full_name,
            "username": updated_user.username,
            "role": updated_user.role,
            "profile_photo": get_profile_photo_url(updated_user.profile_photo),
            "email": getattr(updated_user, "email", None),
            "phone": getattr(updated_user, "phone", None),
            "grade": getattr(updated_user, "grade", None),
            "subject_assigned": getattr(updated_user, "subject_assigned", None)
        }
    }

@router.put("/{user_id}")
async def edit_user(
    user_id: int,
    edit_data: UserEditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Edit user information based on logged-in user's role.
    Permissions:
    - Own profile
    - Teacher: Students in their grade/school
    - EduOffice: Students/Teachers
    - Admin: Anyone
    """
    target_user = get_user_by_id(db, user_id)
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if target_user.role != edit_data.role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot edit {target_user.role} as {edit_data.role}")
    
    if not can_edit_user(current_user, target_user, current_user.role):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    
    updated_user = update_user(db, target_user, edit_data.data, current_user.role)
    return updated_user

# Own profile update remains PUT /profile (existing)
