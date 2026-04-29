from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Schema for Practice Mock Test
class PracticeMockTestBase(BaseModel):
    title: str
    subject: str
    description: Optional[str] = None
    duration_minutes: int = 30
    is_active: bool = True


class PracticeMockTestCreate(PracticeMockTestBase):
    pass


class PracticeMockTestUpdate(BaseModel):
    title: Optional[str] = None
    subject: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    is_active: Optional[bool] = None


class PracticeMockTestResponse(PracticeMockTestBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Schema for Practice Question
class PracticeQuestionBase(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    explanation: Optional[str] = None
    order_index: int = 0


class PracticeQuestionCreate(PracticeQuestionBase):
    mock_test_id: int


class PracticeQuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    order_index: Optional[int] = None


class PracticeQuestionResponse(PracticeQuestionBase):
    id: int
    mock_test_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Combined response with questions
class PracticeMockTestWithQuestions(PracticeMockTestResponse):
    questions: List[PracticeQuestionResponse] = []

    class Config:
        from_attributes = True


# Schema for Practice Mock Attempt
class PracticeAttemptBase(BaseModel):
    student_id: int
    mock_test_id: int


class PracticeAttemptCreate(PracticeAttemptBase):
    pass


class PracticeAttemptUpdate(BaseModel):
    score: int
    total_questions: int
    is_completed: bool = True
    time_taken_seconds: int = 0


class PracticeAttemptResponse(PracticeAttemptBase):
    id: int
    score: int
    total_questions: int
    percentage: float
    started_at: datetime
    completed_at: Optional[datetime] = None
    time_taken_seconds: int
    is_completed: bool

    class Config:
        from_attributes = True


# Schema for submitting practice test answers
class PracticeAnswerSubmit(BaseModel):
    question_id: int
    selected_answer: str


class PracticeTestSubmit(BaseModel):
    attempt_id: int
    answers: List[PracticeAnswerSubmit]
    time_taken_seconds: int = 0
