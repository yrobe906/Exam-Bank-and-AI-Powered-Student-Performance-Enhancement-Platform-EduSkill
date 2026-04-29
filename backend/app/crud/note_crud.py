from sqlalchemy.orm import Session
from app.models.note_models import Note
from app.schemas.note_schemas import NoteCreate, NoteUpdate



def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Note).offset(skip).limit(limit).all()

def get_note(db: Session, note_id: int):
    return db.query(Note).filter(Note.id == note_id).first()

def create_note(db: Session, note_data: dict):
    # Handle both dict and NoteCreate object
    if isinstance(note_data, NoteCreate):
        note_dict = note_data.model_dump()
    else:
        note_dict = note_data
    
    db_note = Note(**note_dict)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_note(db: Session, note_id: int, note_update: NoteUpdate):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        return None
    
    update_data = note_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_note, field, value)
    
    db.commit()
    db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: int):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
        return True
    return False
