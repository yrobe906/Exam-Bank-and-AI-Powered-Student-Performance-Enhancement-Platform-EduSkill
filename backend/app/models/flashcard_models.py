from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from datetime import datetime
from database import Base
import enum

class CardStatus(str, enum.Enum):
    LEARNING = "learning"
    KNOWN = "known"
    REVISIT = "revisit"

class FlashcardDeck(Base):
    __tablename__ = "flashcard_decks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    topic = Column(String(255), nullable=True)
    exam_board = Column(String(50), nullable=True)  # AQA, OCR, Edexcel, WJEC
    description = Column(Text, nullable=True)
    card_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    deck_id = Column(Integer, ForeignKey("flashcard_decks.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserFlashcardProgress(Base):
    __tablename__ = "user_flashcard_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    flashcard_id = Column(Integer, ForeignKey("flashcards.id"), nullable=False)
    status = Column(Enum(CardStatus), default=CardStatus.LEARNING)
    times_reviewed = Column(Integer, default=0)
    last_reviewed = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
