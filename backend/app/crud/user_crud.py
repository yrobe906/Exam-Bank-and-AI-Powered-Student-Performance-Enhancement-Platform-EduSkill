from sqlalchemy.orm import Session
from sqlalchemy import update
from typing import Optional, Dict, Any
from datetime import datetime
from ..models.user_models import User
from ..schemas.user_edit_schemas import UserEditBase, UserEditStudent, UserEditTeacher, UserEditEduoffice

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Get user by ID.
    """
    return db.query(User).filter(User.id == user_id).first()

def update_user(
    db: Session, 
    db_user: User, 
    obj_in: Dict[str, Any],
    updated_by_role: str
) -> User:
    """
    Update user fields based on role permissions.
    
    Args:
        db_user: User from DB
        obj_in: Dict of fields to update
        updated_by_role: Role of logged-in user ('student', 'teacher', etc.)
    
    Returns:
        Updated User object
    """
    # Common fields anyone can edit (own profile)
    allowed_self = {"full_name", "gender", "username", "email", "phone", "profile_photo"}
    
    # Role-specific self-editable fields
    if db_user.role == "student":
        allowed_self.update({"school_id", "grade"})
    elif db_user.role == "teacher":
        allowed_self.update({"school_name", "subject_assigned", "teaching_grade"})
    elif db_user.role == "eduoffice":
        allowed_self.update({"woreda", "school_supervising"})
    
    # If self-update (same role), allow self fields
    if updated_by_role == db_user.role:
        allowed_fields = allowed_self
    else:
        # Admin editing others
        allowed_fields = allowed_self.copy()
        if updated_by_role in ["teacher", "eduoffice", "admin"]:
            allowed_fields.update({"school_id", "grade"})
        if updated_by_role in ["eduoffice", "admin"]:
            allowed_fields.update({"phone", "school_name", "subject_assigned", "teaching_grade"})
        if updated_by_role == "admin":
            allowed_fields.update({"woreda", "school_supervising"})
    
    # Filter only allowed fields
    update_data = {k: v for k, v in obj_in.items() if k in allowed_fields}
    
    # Add updated timestamp if DB supports
    if hasattr(db_user, 'updated_at'):
        update_data['updated_at'] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Permission check helper (used in router)
def can_edit_user(
    current_user: User, 
    target_user: User, 
    current_role: str
) -> bool:
    """
    Check if current_user can edit target_user based on roles.
    """
    if current_user.id == target_user.id:
        return True  # Own profile
    
    if current_role == "admin":
        return True
    
    if current_role == "teacher" and target_user.role == "student":
        # Teacher can edit students in their grade/school
        return (
            target_user.grade == current_user.teaching_grade and
            target_user.school_id == current_user.school_name
        )
    
    if current_role == "eduoffice":
        # Eduoffice can edit students/teachers
        return target_user.role in ["student", "teacher"]
    
    return False

