from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from app.models.user_models import User
from app.models.admin import Admin
import os

# JWT settings (matching login endpoints)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/admin/login")  # or /api/users/login

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        username: str = payload.get("username")
        role: str = payload.get("role")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Query User first (for student/teacher/eduoffice)
    user = db.query(User).filter(User.id == int(user_id), User.status == "approved").first()
    if user and role == user.role:
        return user
    
    # Fallback to Admin (for admin role)
    admin = db.query(Admin).filter(Admin.id == int(user_id), Admin.is_active == True).first()
    if admin and role == "admin":
        # Return as User type for dependency (admin acts as User for auth)
        return User(
            id=admin.id,
            username=admin.username,
            full_name=admin.full_name,
            role="admin",
            status="approved" if admin.is_active else "inactive"
        )
    
    raise credentials_exception
