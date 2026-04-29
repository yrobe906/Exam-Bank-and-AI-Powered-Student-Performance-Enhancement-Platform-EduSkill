# app/auth.py
from fastapi import Header, HTTPException, Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database import get_db
from app.models.user_models import User  # ✅ Correct import
from app.models.admin import Admin  # Import Admin model
import os

# Use same SECRET_KEY as admin_router.py
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"


# ================= ADMIN AUTH =================
def get_current_admin(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role", "")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token decode error")

    # Check if it's an admin token (from admin login)
    if role == "admin":
        # Look up in Admin table
        admin = db.query(Admin).filter(Admin.id == int(user_id)).first()
        if admin:
            # Return a mock user object with admin role for compatibility
            mock_user = type('User', (), {
                'id': admin.id,
                'role': 'admin',
                'username': admin.username,
                'email': admin.email
            })()
            return mock_user
    
    # Otherwise check User table for admin role
    user = db.query(User).filter(User.id == user_id).first()

    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Not an admin")

    return user


# ================= ADMIN OR TEACHER AUTH =================
def get_current_admin_or_teacher(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role", "")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token decode error")

    # Check if it's an admin token (from admin login)
    if role == "admin":
        # Look up in Admin table
        admin = db.query(Admin).filter(Admin.id == int(user_id)).first()
        if admin:
            # Return a mock user object with admin role for compatibility
            mock_user = type('User', (), {
                'id': admin.id,
                'role': 'admin',
                'username': admin.username,
                'email': admin.email
            })()
            return mock_user
    
    # Otherwise check User table for admin or teacher role
    user = db.query(User).filter(User.id == user_id).first()

    if not user or (user.role != "admin" and user.role != "teacher"):
        raise HTTPException(status_code=403, detail="Not authorized")

    return user


# ================= USER AUTH =================
def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role", "")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check if it's an admin token (from admin login)
    if role == "admin":
        # Look up in Admin table first
        admin = db.query(Admin).filter(Admin.id == int(user_id)).first()
        if admin:
            # Return a mock user object with admin role
            mock_user = type('User', (), {
                'id': admin.id,
                'role': 'admin',
                'username': admin.username,
                'email': admin.email,
                'full_name': admin.full_name
            })()
            return mock_user
    
    # For regular users, look up in User table
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ================= ADMIN USER AUTH (For explicit admin endpoints) =================
def get_current_admin_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Authentication function specifically for admin endpoints.
    Properly handles both:
    1. Admin tokens from Admin table (admin login)
    2. User tokens with admin role from User table
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role", "")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check if it's an admin token (from admin login)
    if role == "admin":
        # Look up in Admin table
        admin = db.query(Admin).filter(Admin.id == int(user_id)).first()
        if admin:
            # Return a mock user object with admin role
            mock_user = type('User', (), {
                'id': admin.id,
                'role': 'admin',
                'username': admin.username,
                'email': admin.email,
                'full_name': admin.full_name
            })()
            return mock_user
        # If admin not found in Admin table, check User table
        user = db.query(User).filter(User.id == user_id, User.role == "admin").first()
        if user:
            return user
        raise HTTPException(status_code=403, detail="Admin not found")
    
    # Check User table for admin role
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return user


# ================= EDUOFFICE AUTH =================
def get_current_eduoffice(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role", "")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check if it's an admin token (from admin login) - temporarily allow for testing
    if role == "admin":
        # Look up in Admin table
        admin = db.query(Admin).filter(Admin.id == int(user_id)).first()
        if admin:
            # Return a mock user object with eduoffice role for compatibility
            mock_user = type('User', (), {
                'id': admin.id,
                'role': 'eduoffice',  # Treat admin as eduoffice
                'username': admin.username,
                'email': admin.email,
                'full_name': admin.full_name
            })()
            return mock_user
        # If admin not found in Admin table, check User table
        user = db.query(User).filter(User.id == user_id, User.role == "admin").first()
        if user:
            user.role = "eduoffice"  # Temporarily change role for this request
            return user
        raise HTTPException(status_code=403, detail="Admin not found")

    # Check User table for eduoffice role
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role != "eduoffice":
        raise HTTPException(status_code=403, detail="EduOffice access required")

    return user
