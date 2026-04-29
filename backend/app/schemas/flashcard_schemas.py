from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class CardStatus(str, Enum):
    LEARNING = "learning"
    KNOWN = "known"
    REVISIT = "revisit"

# Flashcard Deck Schemas
class FlashcardDeckBase(BaseModel):
    name: str
    subject: str
    topic: Optional[str] = None
    exam_board: Optional[str] = None
    description: Optional[str] = None

class FlashcardDeckCreate(FlashcardDeckBase):
    pass

class FlashcardDeckUpdate(BaseModel):
    name: Optional[str] = None
    topic: Optional[str] = None
    exam_board: Optional[str] = None
    description: Optional[str] = None
    card_count: Optional[int] = None

class FlashcardDeckResponse(FlashcardDeckBase):
    id: int
    card_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Flashcard Schemas
class FlashcardBase(BaseModel):
    question: str
    answer: str
    order_index: int = 0

class FlashcardCreate(FlashcardBase):
    deck_id: int

class FlashcardUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    order_index: Optional[int] = None

class FlashcardResponse(FlashcardBase):
    id: int
    deck_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FlashcardWithProgress(FlashcardResponse):
    status: Optional[CardStatus] = None
    times_reviewed: Optional[int] = 0

    class Config:
        from_attributes = True

# User Progress Schemas
class UserFlashcardProgressBase(BaseModel):
    flashcard_id: int
    status: CardStatus = CardStatus.LEARNING

class UserFlashcardProgressUpdate(BaseModel):
    status: CardStatus

class UserFlashcardProgressResponse(UserFlashcardProgressBase):
    id: int
    user_id: int
    times_reviewed: int
    last_reviewed: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Deck with Cards
class FlashcardDeckWithCards(FlashcardDeckResponse):
    cards: List[FlashcardResponse] = []

    class Config:
        from_attributes = True

# Statistics
class FlashcardStats(BaseModel):
    total_decks: int
    total_cards: int
    learning_count: int
    known_count: int
    revisit_count: int

class DeckStats(BaseModel):
    deck_id: int
    deck_name: str
    total_cards: int
    learning_count: int
    known_count: int
    revisit_count: int
