from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime

from database import get_db
from app.auth import get_current_user
from app.models.user_models import User
from ..schemas.user_edit_schemas import (
    UserEditRequest, UserEditResponse
)
from ..crud.user_crud import (
    get_user_by_id, update_user, can_edit_user
)

router = APIRouter()

@router.put("/{user_id}", response_model=UserEditResponse)
async def edit_user(
    user_id: int,
    edit_data: UserEditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Edit user information based on logged-in user's role.
    
    Permissions:
    - Anyone: Own profile (common fields: full_name, gender)
    - Teacher: Students in their grade + school
    - EduOffice: Any student/teacher  
    - Admin: Anyone
    
    Request body example:
    {
        "role": "student",
        "data": {
            "full_name": "New Name",
            "gender": "male", 
            "school_id": "SCH001",
            "grade": 10
        }
    }
    """
    # Get target user
    target_user = get_user_by_id(db, user_id)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Validate target role matches request
    if target_user.role != edit_data.role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot edit {target_user.role} user with {edit_data.role} schema"
        )
    
    # Permission check
    if not can_edit_user(current_user, target_user, current_user.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to edit this user"
        )
    
    # Update user
    updated_user = update_user(
        db, target_user, edit_data.data, 
        current_user.role  # Pass role for field filtering
    )
    
    return updated_user

