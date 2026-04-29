from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from app.models.flashcard_models import FlashcardDeck, Flashcard, UserFlashcardProgress, CardStatus
from app.schemas.flashcard_schemas import (
    FlashcardDeckCreate, FlashcardDeckUpdate,
    FlashcardCreate, FlashcardUpdate,
    UserFlashcardProgressUpdate
)

# ==================== Deck CRUD ====================

def create_deck(db: Session, deck: FlashcardDeckCreate) -> FlashcardDeck:
    db_deck = FlashcardDeck(**deck.dict())
    db.add(db_deck)
    db.commit()
    db.refresh(db_deck)
    return db_deck

def get_deck(db: Session, deck_id: int) -> Optional[FlashcardDeck]:
    return db.query(FlashcardDeck).filter(FlashcardDeck.id == deck_id).first()

def get_decks(db: Session, skip: int = 0, limit: int = 100) -> List[FlashcardDeck]:
    return db.query(FlashcardDeck).offset(skip).limit(limit).all()

def get_decks_by_subject(db: Session, subject: str, exam_board: Optional[str] = None) -> List[FlashcardDeck]:
    query = db.query(FlashcardDeck).filter(FlashcardDeck.subject == subject)
    if exam_board:
        query = query.filter(FlashcardDeck.exam_board == exam_board)
    return query.all()

def get_all_subjects(db: Session) -> List[str]:
    return db.query(FlashcardDeck.subject).distinct().all()

def update_deck(db: Session, deck_id: int, deck: FlashcardDeckUpdate) -> Optional[FlashcardDeck]:
    db_deck = get_deck(db, deck_id)
    if not db_deck:
        return None
    
    for key, value in deck.dict(exclude_unset=True).items():
        setattr(db_deck, key, value)
    
    db_deck.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_deck)
    return db_deck

def delete_deck(db: Session, deck_id: int) -> bool:
    db_deck = get_deck(db, deck_id)
    if not db_deck:
        return False
    
    # First delete all associated flashcards and their progress
    flashcards = db.query(Flashcard).filter(Flashcard.deck_id == deck_id).all()
    for card in flashcards:
        # Delete progress records for each flashcard
        db.query(UserFlashcardProgress).filter(
            UserFlashcardProgress.flashcard_id == card.id
        ).delete()
        db.delete(card)
    
    # Also delete any progress records that might be orphaned
    db.query(UserFlashcardProgress).filter(
        UserFlashcardProgress.flashcard_id.in_(
            db.query(Flashcard.id).filter(Flashcard.deck_id == deck_id)
        )
    ).delete(synchronize_session=False)
    
    # Now delete the deck
    db.delete(db_deck)
    db.commit()
    return True

def update_deck_card_count(db: Session, deck_id: int):
    db_deck = get_deck(db, deck_id)
    if db_deck:
        count = db.query(Flashcard).filter(Flashcard.deck_id == deck_id).count()
        db_deck.card_count = count
        db.commit()

# ==================== Flashcard CRUD ====================

def create_flashcard(db: Session, flashcard: FlashcardCreate) -> Flashcard:
    db_flashcard = Flashcard(**flashcard.dict())
    db.add(db_flashcard)
    db.commit()
    
    # Update deck card count
    update_deck_card_count(db, flashcard.deck_id)
    
    db.refresh(db_flashcard)
    return db_flashcard

def create_flashcards_bulk(db: Session, flashcards: List[FlashcardCreate]) -> List[Flashcard]:
    db_flashcards = []
    deck_id = None
    
    for flashcard in flashcards:
        db_flashcard = Flashcard(**flashcard.dict())
        db.add(db_flashcard)
        db_flashcards.append(db_flashcard)
        deck_id = flashcard.deck_id
    
    db.commit()
    
    # Refresh all and update deck count
    for flashcard in db_flashcards:
        db.refresh(flashcard)
    
    if deck_id:
        update_deck_card_count(db, deck_id)
    
    return db_flashcards

def get_flashcard(db: Session, flashcard_id: int) -> Optional[Flashcard]:
    return db.query(Flashcard).filter(Flashcard.id == flashcard_id).first()

def get_flashcards_by_deck(db: Session, deck_id: int) -> List[Flashcard]:
    return db.query(Flashcard).filter(Flashcard.deck_id == deck_id).order_by(Flashcard.order_index).all()

def update_flashcard(db: Session, flashcard_id: int, flashcard: FlashcardUpdate) -> Optional[Flashcard]:
    db_flashcard = get_flashcard(db, flashcard_id)
    if not db_flashcard:
        return None
    
    for key, value in flashcard.dict(exclude_unset=True).items():
        setattr(db_flashcard, key, value)
    
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard

def delete_flashcard(db: Session, flashcard_id: int) -> bool:
    db_flashcard = get_flashcard(db, flashcard_id)
    if not db_flashcard:
        return False
    
    deck_id = db_flashcard.deck_id
    db.delete(db_flashcard)
    db.commit()
    
    # Update deck card count
    update_deck_card_count(db, deck_id)
    
    return True

# ==================== User Progress CRUD ====================

def get_or_create_progress(db: Session, user_id: int, flashcard_id: int) -> UserFlashcardProgress:
    progress = db.query(UserFlashcardProgress).filter(
        UserFlashcardProgress.user_id == user_id,
        UserFlashcardProgress.flashcard_id == flashcard_id
    ).first()
    
    if not progress:
        progress = UserFlashcardProgress(
            user_id=user_id,
            flashcard_id=flashcard_id,
            status=CardStatus.LEARNING
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
    
    return progress

def update_progress(db: Session, user_id: int, flashcard_id: int, status: CardStatus) -> Optional[UserFlashcardProgress]:
    progress = get_or_create_progress(db, user_id, flashcard_id)
    progress.status = status
    progress.times_reviewed += 1
    progress.last_reviewed = datetime.utcnow()
    progress.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(progress)
    return progress

def get_user_progress_for_deck(db: Session, user_id: int, deck_id: int) -> List[UserFlashcardProgress]:
    flashcard_ids = [f.id for f in get_flashcards_by_deck(db, deck_id)]
    return db.query(UserFlashcardProgress).filter(
        UserFlashcardProgress.user_id == user_id,
        UserFlashcardProgress.flashcard_id.in_(flashcard_ids)
    ).all()

def get_deck_stats(db: Session, user_id: int, deck_id: int) -> dict:
    flashcards = get_flashcards_by_deck(db, deck_id)
    flashcard_ids = [f.id for f in flashcards]
    
    if not flashcard_ids:
        return {
            "deck_id": deck_id,
            "total_cards": 0,
            "learning_count": 0,
            "known_count": 0,
            "revisit_count": 0
        }
    
    progress = db.query(UserFlashcardProgress).filter(
        UserFlashcardProgress.user_id == user_id,
        UserFlashcardProgress.flashcard_id.in_(flashcard_ids)
    ).all()
    
    learning = sum(1 for p in progress if p.status == CardStatus.LEARNING)
    known = sum(1 for p in progress if p.status == CardStatus.KNOWN)
    revisit = sum(1 for p in progress if p.status == CardStatus.REVISIT)
    
    return {
        "deck_id": deck_id,
        "total_cards": len(flashcards),
        "learning_count": learning,
        "known_count": known,
        "revisit_count": revisit
    }

def get_user_stats(db: Session, user_id: int) -> dict:
    total_cards = db.query(Flashcard).count()
    
    progress = db.query(UserFlashcardProgress).filter(
        UserFlashcardProgress.user_id == user_id
    ).all()
    
    learning = sum(1 for p in progress if p.status == CardStatus.LEARNING)
    known = sum(1 for p in progress if p.status == CardStatus.KNOWN)
    revisit = sum(1 for p in progress if p.status == CardStatus.REVISIT)
    
    return {
        "total_cards": total_cards,
        "learning_count": learning,
        "known_count": known,
        "revisit_count": revisit
    }
