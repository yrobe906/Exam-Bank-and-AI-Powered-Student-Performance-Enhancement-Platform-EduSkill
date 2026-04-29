from fastapi import APIRouter, Depends, HTTPException, Body, Form, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from jose import jwt
import os
from passlib.context import CryptContext

from database import get_db
from app.models.admin import Admin
from app.models.user_models import User
from app.models.sector_models import SectorModel
from app.models.exam_models import ExamModel  # This is correct - your model is named ExamModel
from app.schemas.exam_schemas import SectorOut, ExamOut
from app.models.exam_attempt_models import ExamAttemptModel
from app.models.analytics_models import StudentOverallAnalytics, StudentSubjectAnalytics, StudentTopicAnalytics
# Removed the incorrect import: from app.models.exam_models import Exam

router = APIRouter(
    tags=["Admin"]
)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings - should match auth.py
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"


# ✅ Admin Login Endpoint
@router.post("/login")
def admin_login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Admin login - validates credentials and returns JWT token
    """
    # Try to find admin by username or email
    admin = db.query(Admin).filter(
        (Admin.username == username) | (Admin.email == username)
    ).first()
    
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not pwd_context.verify(password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not admin.is_active:
        raise HTTPException(status_code=403, detail="Admin account is inactive")
    
    # Create JWT token
    token_data = {
        "sub": str(admin.id),
        "username": admin.username,
        "role": "admin"
    }
    
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "admin_id": admin.id,
        "username": admin.username,
        "full_name": admin.full_name
    }

# ✅ 1. Get all users whose status is "pending"
@router.get("/pending-users")
def get_pending_users(db: Session = Depends(get_db)):
    pending_users = db.query(User).filter(User.status == "pending").all()

    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        }
        for user in pending_users
    ]


# ✅ 2. Approve or Reject user
@router.patch("/update-status/{user_id}")
def update_user_status(user_id: int, data: dict = Body(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_status = data.get("status")

    if new_status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    user.status = new_status
    db.commit()

    return {"message": f"User {new_status} successfully"}


# ✅ 3. Get all users with optional filters
@router.get("/all-users")
def get_all_users(
    role: str = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """
    Get all users with optional role and status filters
    """
    query = db.query(User)
    
    if role:
        query = query.filter(User.role == role)
    if status:
        query = query.filter(User.status == status)
    
    users = query.all()
    
    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "gender": user.gender,
            "phone_number": user.phone,
            "status": user.status,
            "profile_photo": user.profile_photo,
            "schoolid": user.school_id,
            "grade": user.grade,
            "subject_assigned": user.subject_assigned,
            "teaching_grade": user.teaching_grade,
            "school_name": user.school_name,
            "school_supervising": user.school_supervising,
            "woreda": user.woreda,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
        for user in users
    ]


# ✅ 4. Delete a user
@router.delete("/delete-user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by ID - handles related records first to avoid FK constraint
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        # First delete related analytics records
        overall_analytics = db.query(StudentOverallAnalytics).filter(StudentOverallAnalytics.student_id == user.id).all()
        for record in overall_analytics:
            db.delete(record)
        
        subject_analytics = db.query(StudentSubjectAnalytics).filter(StudentSubjectAnalytics.student_id == user.id).all()
        for record in subject_analytics:
            db.delete(record)
        
        topic_analytics = db.query(StudentTopicAnalytics).filter(StudentTopicAnalytics.student_id == user.id).all()
        for record in topic_analytics:
            db.delete(record)
        
        # Then delete the user
        db.delete(user)
        db.commit()
        
        return {"message": "User deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")


# ✅ 5. Get single user details
@router.get("/user/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a single user by ID
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "gender": user.gender,
        "phone_number": user.phone,
        "status": user.status,
        "profile_photo": user.profile_photo,
        "schoolid": user.school_id,
        "grade": user.grade,
        "subject_assigned": user.subject_assigned,
        "teaching_grade": user.teaching_grade,
        "school_name": user.school_name,
        "school_supervising": user.school_supervising,
        "woreda": user.woreda,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }


# ✅ 6. Update user details
@router.put("/edit-user/{user_id}")
def edit_user(
    user_id: int,
    full_name: str = Body(None),
    email: str = Body(None),
    role: str = Body(None),
    gender: str = Body(None),
    phone: str = Body(None),
    school_id: str = Body(None),
    grade: int = Body(None),
    subject_assigned: str = Body(None),
    teaching_grade: int = Body(None),
    school_name: str = Body(None),
    school_supervising: str = Body(None),
    woreda: str = Body(None),
    db: Session = Depends(get_db)
):
    """
    Update user details
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields if provided
    if full_name is not None:
        user.full_name = full_name
    if email is not None:
        # Check if email is already taken by another user
        existing = db.query(User).filter(User.email == email, User.id != user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")
        user.email = email
    if role is not None:
        user.role = role
    if gender is not None:
        user.gender = gender
    if phone is not None:
        user.phone = phone
    if school_id is not None:
        user.school_id = school_id
    if grade is not None:
        user.grade = grade
    if subject_assigned is not None:
        user.subject_assigned = subject_assigned
    if teaching_grade is not None:
        user.teaching_grade = teaching_grade
    if school_name is not None:
        user.school_name = school_name
    if school_supervising is not None:
        user.school_supervising = school_supervising
    if woreda is not None:
        user.woreda = woreda
    
    db.commit()
    db.refresh(user)
    
    return {"message": "User updated successfully", "user_id": user.id}


# ✅ 9. Get Section Leaderboard - All Sections with Stats
@router.get("/analytics/section-leaderboard")
def get_section_leaderboard(
    grade_level: int = None,
    section_category: str = None,
    db: Session = Depends(get_db)
):
    """
    Get section leaderboard with performance stats.
    - grade_level: Filter by specific grade (9, 10, 11, 12)
    - section_category: Filter by subject category (e.g., 'Natural Science', 'Social Science')
    
    Returns sections ranked by weighted score.
    """
    from app.models.exam_models import Exam
    from app.models.exam_attempt_models import ExamAttemptModel
    from app.models.analytics_models import StudentSubjectAnalytics
    
    # Get all unique subjects from exams
    exams = db.query(Exam).filter(Exam.is_published == True).all()
    
    # Build a list of unique sections (subjects)
    sections_data = {}
    
    for exam in exams:
        section_name = exam.subject
        if not section_name:
            continue
            
        # Apply filters
        if grade_level and exam.grade != grade_level:
            continue
            
        if section_category and section_category != section_category:  # Need to check category mapping
            pass  # For now, allow all
        
        if section_name not in sections_data:
            sections_data[section_name] = {
                "section_name": section_name,
                "section_id": exam.id,
                "sector_name": exam.subject,  # Using subject as sector for now
                "color": get_section_color(section_name),
                "total_exam_attempts": 0,
                "unique_students": set(),
                "exams_count": 0,
                "total_score": 0,
                "weighted_score": 0,
                "average_score": 0
            }
        
        # Get attempts for this exam
        attempts = db.query(ExamAttemptModel).filter(
            ExamAttemptModel.exam_id == exam.id,
            ExamAttemptModel.completed_at != None
        ).all()
        
        sections_data[section_name]["exams_count"] += 1
        sections_data[section_name]["total_exam_attempts"] += len(attempts)
        
        for attempt in attempts:
            sections_data[section_name]["unique_students"].add(attempt.student_id)
            sections_data[section_name]["total_score"] += attempt.score
    
    # Calculate final metrics
    result_sections = []
    for section_name, data in sections_data.items():
        # Normalize attempts (divide by number of exams to get average per exam)
        if data["exams_count"] > 0:
            normalized_attempts = data["total_exam_attempts"] / data["exams_count"]
            data["normalized_attempts"] = round(normalized_attempts, 1)
        else:
            data["normalized_attempts"] = 0
        
        # Calculate average score
        if data["total_exam_attempts"] > 0:
            data["average_score"] = round(data["total_score"] / data["total_exam_attempts"], 1)
        else:
            data["average_score"] = 0
        
        # Calculate weighted score (average_score normalized by attempts)
        # Higher attempts with good scores = better ranking
        if data["average_score"] > 0:
            # Weight = average_score * min(attempts/10, 1) - gives bonus for more attempts
            attempt_weight = min(data["total_exam_attempts"] / 10, 1)
            data["weighted_score"] = round(data["average_score"] * (0.7 + 0.3 * attempt_weight), 1)
        else:
            data["weighted_score"] = 0
        
        # Convert unique_students set to count
        data["unique_students"] = len(data["unique_students"])
        
        # Remove internal data
        result_sections.append(data)
    
    # Sort by weighted score descending
    result_sections.sort(key=lambda x: x["weighted_score"], reverse=True)
    
    # Add rank
    for idx, section in enumerate(result_sections):
        section["rank"] = idx + 1
    
    return {"sections": result_sections}


# ✅ 10. Get Available Grades for Section Leaderboard
@router.get("/analytics/section-leaderboard/grades")
def get_section_leaderboard_grades(db: Session = Depends(get_db)):
    """
    Get available grades that have exam data for section leaderboard.
    """
    from app.models.exam_models import Exam
    
    # Get unique grades from published exams
    grades = db.query(Exam.grade).filter(
        Exam.is_published == True
    ).distinct().all()
    
    return {"grades": [g[0] for g in grades if g[0] in [9, 10, 11, 12]]}


# ✅ 11. Get Available Categories for Section Leaderboard
@router.get("/analytics/section-leaderboard/categories")
def get_section_leaderboard_categories(db: Session = Depends(get_db)):
    """
    Get available subject categories for section leaderboard filters.
    """
    from app.models.exam_models import Exam
    
    # Get unique subjects from published exams
    subjects = db.query(Exam.subject).filter(
        Exam.is_published == True,
        Exam.subject != None
    ).distinct().all()
    
    # Group subjects into categories (simplified)
    categories = []
    for s in subjects:
        if s[0]:
            categories.append({"name": s[0], "count": 1})
    
    return {"categories": categories}


# ✅ 12. Get Section Details - Exam Breakdown
@router.get("/analytics/section-leaderboard/{section_name}/details")
def get_section_details(
    section_name: str,
    grade_level: int = None,
    db: Session = Depends(get_db)
):
    """
    Get detailed exam breakdown for a specific section/subject.
    """
    from app.models.exam_models import Exam
    from app.models.exam_attempt_models import ExamAttemptModel
    
    # Get exams for this subject
    query = db.query(Exam).filter(
        Exam.subject == section_name,
        Exam.is_published == True
    )
    
    if grade_level:
        query = query.filter(Exam.grade == grade_level)
    
    exams = query.all()
    
    exam_details = []
    
    for exam in exams:
        # Get attempts for this exam
        attempts = db.query(ExamAttemptModel).filter(
            ExamAttemptModel.exam_id == exam.id,
            ExamAttemptModel.completed_at != None
        ).all()
        
        total_attempts = len(attempts)
        total_score = sum(a.score for a in attempts)
        avg_score = round(total_score / total_attempts, 1) if total_attempts > 0 else 0
        
        exam_details.append({
            "exam_id": exam.id,
            "exam_name": exam.title,
            "sector_name": exam.subject,
            "total_questions": exam.total_questions or 0,
            "total_attempts": total_attempts,
            "average_score": avg_score
        })
    
    # Sort by average score descending
    exam_details.sort(key=lambda x: x["average_score"], reverse=True)
    
    return {"exams": exam_details}


# ✅ 13. Get Unlock Requests for Admin Review
@router.get("/unlock/requests")
def get_unlock_requests(
    status: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db)
):
    """
    Get unlock requests for admin review.
    Query params:
    - status: 'pending', 'approved', 'rejected' (optional)
    - limit: max number of requests to return (default 100, max 500)
    """
    from app.models.admin import AdminUnlockRequest
    from app.schemas.admin_schemas import AdminUnlockRequestResponse

    query = db.query(AdminUnlockRequest)
    if status:
        query = query.filter(AdminUnlockRequest.status == status)

    requests = query.order_by(AdminUnlockRequest.created_at.desc()).limit(limit).all()

    return [AdminUnlockRequestResponse.from_orm(request) for request in requests]


# ✅ 14. Process Unlock Request (Approve/Reject)
@router.put("/unlock/requests/{request_id}/process")
def process_unlock_request(
    request_id: int,
    action: str = Form(...),
    method: Optional[str] = Form(None),
    transaction_ref: Optional[str] = Form(None),
    admin_notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Process an unlock request (approve or reject).
    Form params:
    - action: 'approve' or 'reject'
    - method: payment method for approval (optional)
    - transaction_ref: transaction reference (optional)
    - admin_notes: admin notes (optional)
    """
    from app.models.admin import AdminUnlockRequest, UserPremiumAccess
    from datetime import datetime

    # Get the request
    request = db.query(AdminUnlockRequest).filter(AdminUnlockRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Unlock request not found")

    if request.status != "pending":
        raise HTTPException(status_code=400, detail=f"Request is already {request.status}")

    # Update the request
    request.status = "approved" if action == "approve" else "rejected"
    request.admin_notes = admin_notes
    request.processed_at = datetime.utcnow()
    # TODO: Set processed_by when we have admin authentication

    # If approved, grant premium access
    if action == "approve":
        premium_access = UserPremiumAccess(
            user_id=request.user_id,
            content_type=request.content_type,
            content_id=request.content_id,
            payment_method=method or "admin_approval"
        )
        db.add(premium_access)

    db.commit()

    return {"message": f"Request {action}d successfully", "request_id": request_id}


# Helper function to get section color
def get_section_color(section_name: str) -> str:
    """Generate consistent color for each section/subject"""
    colors = {
        "Mathematics": "#3b82f6",
        "Physics": "#8b5cf6",
        "Chemistry": "#10b981",
        "Biology": "#f59e0b",
        "English": "#ef4444",
        "Geography": "#06b6d4",
        "History": "#ec4899",
        "Civics": "#6366f1",
        "Economics": "#14b8a6",
        "Technical Drawing": "#f97316",
        "Physical Education": "#84cc16",
        "Art": "#d946ef"
    }
    return colors.get(section_name, "#64748b")  # Default gray
