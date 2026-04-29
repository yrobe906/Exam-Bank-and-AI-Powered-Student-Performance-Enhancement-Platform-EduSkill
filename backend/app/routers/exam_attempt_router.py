# app/routers/exam_attempt_router.py
# NOTE: This router is currently not in use
# The exam attempt functionality is handled by question_router.py
# This file is kept for future use if needed

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from database import get_db
from app.models import exam_attempt_models, student_answer_models
from app.models.exam_models import ExamModel
from app.models.section_models import SectionModel
from app.models.question_models import QuestionModel
from datetime import datetime

# Router commented out to avoid conflict with question_router.py
# The endpoints for exam attempts are already defined in question_router.py
# router = APIRouter(prefix="/api/exam", tags=["Exam Attempt"])

# @router.post("/{exam_id}/start")
# async def start_exam(...)

# NOTE: These endpoints are duplicates of question_router.py
# They are commented out to avoid conflicts
# Use question_router.py for exam attempt functionality

# @router.post("/attempt/{attempt_id}/answer")
# async def save_answer(...)

# @router.post("/attempt/{attempt_id}/submit")
# async def submit_exam(...)
