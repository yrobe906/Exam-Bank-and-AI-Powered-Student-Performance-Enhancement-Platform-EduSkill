# main.py - Update the router includes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.models import *   # very important

# Database
from database import SessionLocal, engine, Base

# Routers
from app.routers import admin_router_fixed as admin_router, resource_router
from app.routers import eduoffice_router
from app.routers.user_router_fixed import router as user_router
from app.routers import AddExamStructure_router, AddQuestion_router
from app.routers import exam_router
from app.routers import question_router
from app.routers import exam_routes  # Import your router
# exam_attempt_router is commented out - question_router handles all exam attempt functionality
from app.routers import analytics_router
from app.routers import flashcard_router
from app.routers import practice_mock_router
from app.routers import forum_router
from app.routers import note_router
from app.routers import ai_router
from app.routers import gamification_router
from app.routers import section_feedback_router
from app.routers import unlock_router_fixed
from app.routers import user_edit_router
from app.routers import password_reset_router
from app.routers import announcement_router

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="EduSkill Hub API",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Upload directories
UPLOAD_DIR = Path("uploads/users")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

RESOURCE_UPLOAD_DIR = Path("uploads/resources")
RESOURCE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
# Serve uploaded profile photos under legacy path as well
app.mount("/uploads/profiles", StaticFiles(directory="uploads"), name="profile_uploads")
# Serve payment proof files
app.mount("/payment_proof", StaticFiles(directory="payment_proof"), name="payment_proof")

app.include_router(admin_router.router, prefix="/api/admin", tags=["Admin"])
app.include_router(eduoffice_router.router, prefix="/api/eduoffice", tags=["EduOffice"])
app.include_router(resource_router.router, prefix="/api/resources", tags=["Resources"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(user_edit_router.router, prefix="/api/users", tags=["User Edit"])
app.include_router(AddExamStructure_router.router, prefix="/api")
app.include_router(AddQuestion_router.router, prefix="/api")
app.include_router(exam_router.router, prefix="/api")
app.include_router(question_router.router, prefix="/api")
app.include_router(exam_routes.router, prefix="/api")  # Make sure prefix is /api
app.include_router(analytics_router.router)
app.include_router(flashcard_router.router, prefix="/api", tags=["Flashcards"])
app.include_router(practice_mock_router.router, tags=["Practice Mock Tests"])
app.include_router(forum_router.router, prefix="/api", tags=["Forum"])
app.include_router(note_router.router)
app.include_router(ai_router.router)
app.include_router(gamification_router.router, prefix="/api/gamification", tags=["Gamification"])
app.include_router(section_feedback_router.router)
app.include_router(unlock_router_fixed.router, prefix="/api", tags=["Unlock"])
app.include_router(password_reset_router.router, prefix="/api/auth", tags=["Password Reset"])
app.include_router(announcement_router.router, prefix="/api/announcements", tags=["Announcements"])


# ---------------- Pydantic models ----------------
from pydantic import BaseModel, EmailStr

class ChatRequest(BaseModel):
    message: str
    user_id: int = None
    context: str = "general"

# ===== AI SERVICE =====
class EducationalAI:
    async def chat(self, message: str):
        responses = {
            "math": "Math tip: Use formulas carefully. Quadratic formula: x = [-b ± √(b² - 4ac)] / 2a",
            "science": "Science tip: Photosynthesis converts light energy to chemical energy.",
            "history": "History fact: Ancient Egypt developed one of the earliest writing systems.",
            "english": "Grammar tip: 'Who' for subjects, 'Whom' for objects.",
            "default": f"I'm here to help you with: '{message}'"
        }
        msg_lower = message.lower()
        if any(w in msg_lower for w in ["math", "algebra", "calculus", "geometry"]):
            return responses["math"]
        elif any(w in msg_lower for w in ["science", "physics", "chemistry", "biology"]):
            return responses["science"]
        elif any(w in msg_lower for w in ["history", "historical", "ancient"]):
            return responses["history"]
        elif any(w in msg_lower for w in ["english", "grammar", "writing"]):
            return responses["english"]
        else:
            return responses["default"]

ai_service = EducationalAI()

# ===== DATABASE DEPENDENCY =====
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===== ROOT ENDPOINT =====
@app.get("/")
def root():
    return {
        "message": "🎓 EduSkill Hub API",
        "status": "running",
        "endpoints": {
            "admin_login": "POST /api/admin/login",
            "user_register": "POST /api/users/register",
            "user_login": "POST /api/users/login",
            "resource_add": "POST /api/resources",
            "resource_list": "GET /api/resources",
            "notes_list": "GET /api/notes",
            "notes_add": "POST /api/notes"
        }

    }

# ===== HEALTH CHECK =====
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# ===== STARTUP EVENT =====
@app.on_event("startup")
async def startup_event():
    print("🚀 EduSkill Hub API Running...")
    print("📚 Docs available at: http://localhost:8000/docs")
    print("🔑 Admin login: POST /api/admin/login")
    print("   Use: email=admin@example.com, password=admin123")

