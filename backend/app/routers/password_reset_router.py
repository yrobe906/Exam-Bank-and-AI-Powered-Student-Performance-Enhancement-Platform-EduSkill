from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os
from pathlib import Path
from dotenv import load_dotenv
from passlib.context import CryptContext

from database import get_db
from app.models.user_models import User
from app.models.password_reset_models import PasswordResetToken
from app.utils.hashing import hash_password

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH, override=True)

router = APIRouter(tags=["Password Reset"])

# Password hashing context (same as existing)
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

# Environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Pydantic models
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

# Helper function to send email
async def send_reset_email(email: str, reset_token: str):
    """Send password reset email via Gmail SMTP"""
    try:
        load_dotenv(ENV_PATH, override=True)
        current_frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

        print(f"📧 Attempting to send reset email to: {email}")
        print(f"🔗 Reset token: {reset_token[:10]}...")
        print(f"🌐 Using FRONTEND_URL from {ENV_PATH}: {current_frontend_url}")

        # Create message
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = email
        msg['Subject'] = "Password Reset Request - EduSkill Hub"

        # Email body
        reset_link = f"{current_frontend_url}/reset-password?token={reset_token}"
        body = f"""
        Hello,

        You have requested to reset your password for EduSkill Hub.

        Please click the following link to reset your password:
        {reset_link}

        This link will expire in 1 hour.

        If you did not request this password reset, please ignore this email.

        Best regards,
        EduSkill Hub Team
        """

        msg.attach(MIMEText(body, 'plain'))

        # Send email
        print("📤 Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        text = msg.as_string()
        server.sendmail(GMAIL_USER, email, text)
        server.quit()

        print(f"✅ Reset email sent successfully to: {email}")

    except Exception as e:
        # Log error but don't raise - we don't want to reveal email sending failures
        print(f"❌ Failed to send reset email: {e}")
        print(f"❌ Error details: {str(e)}")

@router.get("/debug-frontend-url")
async def debug_frontend_url():
    """Debug endpoint to verify the active frontend URL used by password reset emails."""
    current_frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    return {"frontend_url": current_frontend_url, "env_path": str(ENV_PATH)}

@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Handle forgot password request.
    Always returns success message to prevent email enumeration.
    """
    print(f"🔍 Forgot password request for email: {request.email}")

    # Find user by email (case insensitive)
    user = db.query(User).filter(User.email.ilike(request.email)).first()

    if user:
        print(f"✅ User found: {user.email} (ID: {user.id})")

        # Generate secure random token
        reset_token = secrets.token_urlsafe(32)
        print(f"🎫 Generated reset token: {reset_token[:10]}...")

        # Hash the token for storage
        token_hash = pwd_context.hash(reset_token)

        # Set expiry to 1 hour from now (UTC)
        expires_at = datetime.utcnow() + timedelta(hours=1)
        print(f"⏰ Token expires at: {expires_at}")

        # Invalidate previous tokens for this user
        invalidated_count = db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used == False
        ).update({"used": True})
        print(f"🗑️ Invalidated {invalidated_count} previous tokens")

        # Create new token
        new_token = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at
        )
        db.add(new_token)
        db.commit()
        print("💾 New token saved to database")

        # Send email in background
        print("📧 Adding email sending task to background...")
        background_tasks.add_task(send_reset_email, user.email, reset_token)

    else:
        print(f"❌ No user found with email: {request.email}")

    # Always return success message
    print("✅ Returning success response")
    return {"message": "If an account with this email exists, a password reset link has been sent."}

@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Handle password reset using token.
    """
    # Find valid token
    token_record = db.query(PasswordResetToken).filter(
        PasswordResetToken.used == False,
        PasswordResetToken.expires_at > datetime.utcnow()
    ).first()

    if not token_record:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Verify token
    if not pwd_context.verify(request.token, token_record.token_hash):
        raise HTTPException(status_code=400, detail="Invalid token")

    # Get user
    user = db.query(User).filter(User.id == token_record.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    # Hash new password
    hashed_password = hash_password(request.new_password)

    # Update user password
    user.password_hash = hashed_password
    db.add(user)

    # Mark token as used
    token_record.used = True
    db.add(token_record)

    db.commit()

    return {"message": "Password has been reset successfully"}