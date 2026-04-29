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
from app.models.forum_models import ForumPost, ForumPostLike, ForumComment, ForumBookmark
from app.models.section_feedback_models import SectionRating, SectionFeedback
from app.models.practice_mock_models import PracticeMockAttempt
from app.models.password_reset_models import PasswordResetToken
from app.models.gamification_models import GamificationActivityModel
from app.models.flashcard_models import UserFlashcardProgress
from app.models.unlock_models_fixed import UnlockRequestModel, StudentExamUnlockModel
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
    Delete a user by ID - handles all related records first to avoid FK constraint errors
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        # Delete related records in order to avoid foreign key constraint errors
        
        # 1. Forum related records
        forum_posts = db.query(ForumPost).filter(ForumPost.user_id == user.id).all()
        for post in forum_posts:
            # Delete likes, comments, and bookmarks for each post
            db.query(ForumPostLike).filter(ForumPostLike.post_id == post.id).delete()
            db.query(ForumComment).filter(ForumComment.post_id == post.id).delete()
            db.query(ForumBookmark).filter(ForumBookmark.post_id == post.id).delete()
            db.delete(post)
        
        # Delete forum interactions where user is the actor
        db.query(ForumPostLike).filter(ForumPostLike.user_id == user.id).delete()
        db.query(ForumComment).filter(ForumComment.user_id == user.id).delete()
        db.query(ForumBookmark).filter(ForumBookmark.user_id == user.id).delete()
        
        # 2. Exam attempts
        db.query(ExamAttemptModel).filter(ExamAttemptModel.student_id == user.id).delete()
        
        # 3. Section feedback
        db.query(SectionRating).filter(SectionRating.user_id == user.id).delete()
        db.query(SectionFeedback).filter(SectionFeedback.user_id == user.id).delete()
        
        # 4. Practice mock attempts
        db.query(PracticeMockAttempt).filter(PracticeMockAttempt.student_id == user.id).delete()
        
        # 5. Password reset records
        db.query(PasswordResetToken).filter(PasswordResetToken.user_id == user.id).delete()
        
        # 6. Gamification records
        db.query(GamificationActivityModel).filter(GamificationActivityModel.user_id == user.id).delete()
        
        # 7. Flashcard progress
        db.query(UserFlashcardProgress).filter(UserFlashcardProgress.user_id == user.id).delete()
        
        # 8. Unlock requests
        db.query(UnlockRequestModel).filter(UnlockRequestModel.user_id == user.id).delete()
        db.query(StudentExamUnlockModel).filter(StudentExamUnlockModel.user_id == user.id).delete()
        
        # 9. Analytics records
        db.query(StudentOverallAnalytics).filter(StudentOverallAnalytics.student_id == user.id).delete()
        db.query(StudentSubjectAnalytics).filter(StudentSubjectAnalytics.student_id == user.id).delete()
        db.query(StudentTopicAnalytics).filter(StudentTopicAnalytics.student_id == user.id).delete()
        
        # Finally delete the user
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

# Downloadables now use payment-only access, gamification decoupled

# ========== UNLOCK REQUESTS ENDPOINTS ==========
from ..services.unlock_service import service_get_admin_requests, service_process_request, service_verify_payment, service_delete_unlock_request
from ..schemas.unlock_schemas import UnlockRequestAdminOut, ProcessRequest, VerifyPayment
from ..crud.unlock_crud import get_unlock_request
from app.auth import get_current_user
from app.schemas.gamification_schemas import AdminAllRequestsResponse
from app.services.gamification_service_fixed import GamificationService
import logging
logger = logging.getLogger(__name__)
from typing import Optional

get_gamification_service = GamificationService(None)  # db passed later in call

@router.get("/unlock/requests", response_model=List[UnlockRequestAdminOut])
def admin_get_requests(
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return service_get_admin_requests(db, status)

@router.post("/unlock/process/{request_id}")
def admin_process_request(
    request_id: int,
    data: ProcessRequest,
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"Admin processing unlock request {request_id} with action '{data.action}'")
        return service_process_request(db, request_id, data.action, data.method, data.transaction_ref, data.admin_notes)
    except HTTPException as e:
        logger.error(f"HTTP error {e.status_code} on unlock process {request_id}: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error on unlock process {request_id}: {str(e)}", exc_info=True)
        raise HTTPException(500, f"Failed to process unlock request: {str(e)}")

@router.post("/unlock/verify-payment/{request_id}")
def admin_verify_payment(
    request_id: int,
    data: VerifyPayment,
    db: Session = Depends(get_db)
):
    return service_verify_payment(db, request_id, data.verified, data.transaction_ref)

@router.delete("/unlock/{request_id}")
def admin_delete_unlock_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    """
    Admin hard delete unlock request/transaction - removes from database
    """
    return service_delete_unlock_request(db, request_id)



@router.get("/gamification/all-requests", response_model=AdminAllRequestsResponse)
def admin_gamification_requests(
    limit: int = Query(50, ge=1, le=500),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    """
    No auth needed: Get all gamification activities/requests across all users.
    """

    return service.get_all_requests(page=page, limit=limit)

