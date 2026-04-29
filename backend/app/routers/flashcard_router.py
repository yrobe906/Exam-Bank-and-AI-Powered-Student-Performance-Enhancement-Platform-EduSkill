from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
from app.crud import flashcard_crud as crud
from app.schemas.flashcard_schemas import (
    FlashcardDeckCreate, FlashcardDeckUpdate, FlashcardDeckResponse,
    FlashcardCreate, FlashcardUpdate, FlashcardResponse, FlashcardWithProgress,
    UserFlashcardProgressUpdate, UserFlashcardProgressResponse,
    FlashcardDeckWithCards, DeckStats
)
from app.models.flashcard_models import CardStatus
from app.models.user_models import User

router = APIRouter(prefix="/flashcards", tags=["Flashcards"])

# Helper function to get current user (simplified - would use auth in production)
def get_current_user(db: Session = Depends(get_db), user_id: int = Query(None)) -> User:
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ==================== Deck Endpoints ====================

@router.post("/decks", response_model=FlashcardDeckResponse)
def create_deck(deck: FlashcardDeckCreate, db: Session = Depends(get_db)):
    """Create a new flashcard deck"""
    return crud.create_deck(db, deck)

@router.get("/decks", response_model=List[FlashcardDeckResponse])
def get_decks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all flashcard decks"""
    return crud.get_decks(db, skip=skip, limit=limit)

@router.get("/decks/{deck_id}", response_model=FlashcardDeckWithCards)
def get_deck(deck_id: int, db: Session = Depends(get_db)):
    """Get a specific deck with all its cards"""
    deck = crud.get_deck(db, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    
    cards = crud.get_flashcards_by_deck(db, deck_id)
    return {
        **FlashcardDeckResponse.model_validate(deck).model_dump(),
        "cards": cards
    }

@router.get("/subjects/{subject}", response_model=List[FlashcardDeckResponse])
def get_decks_by_subject(
    subject: str,
    exam_board: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all decks for a specific subject"""
    return crud.get_decks_by_subject(db, subject, exam_board)

@router.get("/subjects", response_model=List[str])
def get_all_subjects(db: Session = Depends(get_db)):
    """Get all available subjects"""
    subjects = crud.get_all_subjects(db)
    return [s[0] for s in subjects]

@router.put("/decks/{deck_id}", response_model=FlashcardDeckResponse)
def update_deck(deck_id: int, deck: FlashcardDeckUpdate, db: Session = Depends(get_db)):
    """Update a deck"""
    updated = crud.update_deck(db, deck_id, deck)
    if not updated:
        raise HTTPException(status_code=404, detail="Deck not found")
    return updated

@router.delete("/decks/{deck_id}")
def delete_deck(deck_id: int, db: Session = Depends(get_db)):
    """Delete a deck and all its cards"""
    success = crud.delete_deck(db, deck_id)
    if not success:
        raise HTTPException(status_code=404, detail="Deck not found")
    return {"message": "Deck deleted successfully"}

# ==================== Flashcard Endpoints ====================

@router.post("/cards", response_model=FlashcardResponse)
def create_flashcard(card: FlashcardCreate, db: Session = Depends(get_db)):
    """Create a new flashcard"""
    return crud.create_flashcard(db, card)

@router.post("/cards/bulk", response_model=List[FlashcardResponse])
def create_flashcards_bulk(cards: List[FlashcardCreate], db: Session = Depends(get_db)):
    """Create multiple flashcards at once"""
    return crud.create_flashcards_bulk(db, cards)

@router.get("/decks/{deck_id}/cards", response_model=List[FlashcardResponse])
def get_deck_cards(deck_id: int, db: Session = Depends(get_db)):
    """Get all cards in a deck"""
    deck = crud.get_deck(db, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    return crud.get_flashcards_by_deck(db, deck_id)

@router.get("/cards/{card_id}", response_model=FlashcardResponse)
def get_flashcard(card_id: int, db: Session = Depends(get_db)):
    """Get a specific flashcard"""
    card = crud.get_flashcard(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return card

@router.put("/cards/{card_id}", response_model=FlashcardResponse)
def update_flashcard(card_id: int, card: FlashcardUpdate, db: Session = Depends(get_db)):
    """Update a flashcard"""
    updated = crud.update_flashcard(db, card_id, card)
    if not updated:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return updated

@router.delete("/cards/{card_id}")
def delete_flashcard(card_id: int, db: Session = Depends(get_db)):
    """Delete a flashcard"""
    success = crud.delete_flashcard(db, card_id)
    if not success:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return {"message": "Flashcard deleted successfully"}

# ==================== User Progress Endpoints ====================

@router.get("/decks/{deck_id}/progress", response_model=List[FlashcardWithProgress])
def get_deck_progress(
    deck_id: int,
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Get user's progress for all cards in a deck"""
    deck = crud.get_deck(db, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    
    cards = crud.get_flashcards_by_deck(db, deck_id)
    result = []
    
    for card in cards:
        progress = crud.get_or_create_progress(db, user_id, card.id)
        result.append({
            **FlashcardResponse.model_validate(card).model_dump(),
            "status": progress.status.value if progress.status else CardStatus.LEARNING.value,
            "times_reviewed": progress.times_reviewed
        })
    
    return result

@router.post("/cards/{card_id}/progress")
def update_card_progress(
    card_id: int,
    user_id: int = Query(..., description="User ID"),
    status: CardStatus = Query(..., description="Status: learning, known, or revisit"),
    db: Session = Depends(get_db)
):
    """Update user's progress for a specific card"""
    card = crud.get_flashcard(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    
    progress = crud.update_progress(db, user_id, card_id, status)
    return {
        "message": "Progress updated successfully",
        "status": progress.status.value,
        "times_reviewed": progress.times_reviewed
    }

@router.get("/decks/{deck_id}/stats", response_model=DeckStats)
def get_deck_statistics(
    deck_id: int,
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Get user's statistics for a specific deck"""
    deck = crud.get_deck(db, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    
    stats = crud.get_deck_stats(db, user_id, deck_id)
    stats["deck_name"] = deck.name
    return stats

@router.get("/user/stats")
def get_user_statistics(
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Get overall user's flashcard statistics"""
    return crud.get_user_stats(db, user_id)

# ==================== Seed Data Endpoints (for testing) ====================

@router.post("/seed/sample-decks")
def seed_sample_decks(db: Session = Depends(get_db)):
    """Seed sample flashcard decks for testing"""
    
    # Biology Cell Structure Deck
    biology_deck = crud.create_deck(db, FlashcardDeckCreate(
        name="Cell Structure",
        subject="Biology",
        topic="Cell Biology",
        exam_board="AQA",
        description="Learn about eukaryotic and prokaryotic cells, organelles, and cell membrane structure."
    ))
    
    biology_cards = [
        FlashcardCreate(deck_id=biology_deck.id, question="What are the main characteristics of a eukaryotic organism?", answer="A eukaryotic organism is an organism whose cells contain membrane-bound organelles, including a true nucleus enclosed within a nuclear membrane.", order_index=0),
        FlashcardCreate(deck_id=biology_deck.id, question="What is the function of the mitochondria?", answer="Mitochondria are the powerhouses of the cell, responsible for producing ATP through cellular respiration.", order_index=1),
        FlashcardCreate(deck_id=biology_deck.id, question="What is the difference between prokaryotic and eukaryotic cells?", answer="Prokaryotic cells lack a nucleus and membrane-bound organelles, while eukaryotic cells have a true nucleus and membrane-bound organelles.", order_index=2),
        FlashcardCreate(deck_id=biology_deck.id, question="What is the cell membrane made of?", answer="The cell membrane is made of a phospholipid bilayer with embedded proteins. It is selectively permeable.", order_index=3),
        FlashcardCreate(deck_id=biology_deck.id, question="What is the function of ribosomes?", answer="Ribosomes are responsible for protein synthesis. They translate mRNA into polypeptide chains.", order_index=4),
        FlashcardCreate(deck_id=biology_deck.id, question="What is cell division called in eukaryotes?", answer="Cell division in eukaryotes is called mitosis (for body cells) and meiosis (for sex cells).", order_index=5),
    ]
    crud.create_flashcards_bulk(db, biology_cards)
    
    # Physics Waves Deck
    physics_deck = crud.create_deck(db, FlashcardDeckCreate(
        name="Waves",
        subject="Physics",
        topic="Waves",
        exam_board="AQA",
        description="Learn about transverse and longitudinal waves, wave properties, and electromagnetic spectrum."
    ))
    
    physics_cards = [
        FlashcardCreate(deck_id=physics_deck.id, question="What is a transverse wave?", answer="A transverse wave is one where the oscillations are perpendicular to the direction of energy transfer. Examples include light and water waves.", order_index=0),
        FlashcardCreate(deck_id=physics_deck.id, question="What is a longitudinal wave?", answer="A longitudinal wave is one where the oscillations are parallel to the direction of energy transfer. Examples include sound waves.", order_index=1),
        FlashcardCreate(deck_id=physics_deck.id, question="What is the frequency of a wave?", answer="Frequency is the number of complete waves passing a point per second, measured in Hertz (Hz).", order_index=2),
        FlashcardCreate(deck_id=physics_deck.id, question="What is the wavelength of a wave?", answer="Wavelength is the distance between two consecutive points on a wave that are in phase, such as crest to crest.", order_index=3),
    ]
    crud.create_flashcards_bulk(db, physics_cards)
    
    # Chemistry Atomic Structure Deck
    chemistry_deck = crud.create_deck(db, FlashcardDeckCreate(
        name="Atomic Structure",
        subject="Chemistry",
        topic="Atomic Structure",
        exam_board="AQA",
        description="Learn about atoms, elements, compounds, and the periodic table."
    ))
    
    chemistry_cards = [
        FlashcardCreate(deck_id=chemistry_deck.id, question="What is an atom?", answer="An atom is the smallest part of an element that can exist chemically. It consists of a nucleus containing protons and neutrons, surrounded by electrons.", order_index=0),
        FlashcardCreate(deck_id=chemistry_deck.id, question="What is the atomic number?", answer="The atomic number is the number of protons in the nucleus of an atom. It uniquely identifies an element.", order_index=1),
        FlashcardCreate(deck_id=chemistry_deck.id, question="What is the mass number?", answer="The mass number is the total number of protons and neutrons in the nucleus of an atom.", order_index=2),
    ]
    crud.create_flashcards_bulk(db, chemistry_cards)
    
    # Maths Algebra Deck
    maths_deck = crud.create_deck(db, FlashcardDeckCreate(
        name="Algebra Basics",
        subject="Maths",
        topic="Algebra",
        exam_board="AQA",
        description="Learn about algebraic expressions, equations, and inequalities."
    ))
    
    maths_cards = [
        FlashcardCreate(deck_id=maths_deck.id, question="What is a rational number?", answer="A rational number is any number that can be expressed as a fraction of two integers, where the denominator is not zero.", order_index=0),
        FlashcardCreate(deck_id=maths_deck.id, question="What is an algebraic expression?", answer="An algebraic expression is a mathematical phrase that can contain numbers, variables, and operations (e.g., 3x + 2).", order_index=1),
        FlashcardCreate(deck_id=maths_deck.id, question="How do you solve a linear equation?", answer="To solve a linear equation, isolate the variable on one side by performing the same operation on both sides (e.g., for 2x + 3 = 7, subtract 3 then divide by 2).", order_index=2),
    ]
    crud.create_flashcards_bulk(db, maths_cards)
    
    return {
        "message": "Sample decks created successfully",
        "decks": [
            {"id": biology_deck.id, "name": biology_deck.name, "cards": len(biology_cards)},
            {"id": physics_deck.id, "name": physics_deck.name, "cards": len(physics_cards)},
            {"id": chemistry_deck.id, "name": chemistry_deck.name, "cards": len(chemistry_cards)},
            {"id": maths_deck.id, "name": maths_deck.name, "cards": len(maths_cards)},
        ]
    }
