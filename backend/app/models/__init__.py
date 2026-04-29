# app/models/__init__.py

from .sector_models import SectorModel
from .exam_models import ExamModel
from .section_models import SectionModel
from .question_models import QuestionModel
from .user_models import User

# Import ExamAttemptModel from exam_attempt_models
from .exam_attempt_models import ExamAttemptModel

# Import StudentAnswerModel from student_answer_models
from .student_answer_models import StudentAnswerModel

# Import Analytics Models
from .analytics_models import (
    StudentSubjectAnalytics,
    StudentTopicAnalytics,
    StudentOverallAnalytics,
    StudentProgressHistory,
    AIRecommendation
)

# Import Flashcard Models
from .flashcard_models import FlashcardDeck, Flashcard, UserFlashcardProgress, CardStatus
from .note_models import Note
from .resource_models import Resource

# Import Gamification Models (pure)
from .gamification_models import GamificationActivityModel

# Import Unlock Models (single source - fixed)
from .unlock_models_fixed import UnlockRequestModel, StudentExamUnlockModel

# Import Admin Models
from .admin import Admin, AdminUnlockRequest, UserPremiumAccess

# Import Section Feedback Models
from .section_feedback_models import SectionRating, SectionFeedback

# Import Forum Models
from .forum_models import ForumPost

# Import Password Reset Models
from .password_reset_models import PasswordResetToken

# Import Announcement Models
from .announcement_models import Announcement

