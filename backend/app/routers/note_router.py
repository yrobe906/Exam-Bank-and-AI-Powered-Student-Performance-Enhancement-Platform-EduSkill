from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from app.crud import note_crud
from app.schemas.note_schemas import NoteCreate, NoteUpdate, NoteResponse, LibraryCountsResponse
from app.models.note_models import Note
from app.models.resource_models import Resource


from auth import get_current_admin, get_current_admin_or_teacher


router = APIRouter(
    prefix="/api/notes",
    tags=["notes"]
)

@router.get("/", response_model=List[NoteResponse])
def get_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all notes (public endpoint for students)
    """
    notes = note_crud.get_notes(db, skip=skip, limit=limit)
    return notes


@router.get("/all", response_model=List[NoteResponse])
def get_all_notes_for_admin(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_or_teacher)
):
    """
    Get all notes (admin/teacher only) - includes all notes for management
    """
    notes = note_crud.get_notes(db, skip=skip, limit=limit)
    return notes


@router.get("/library-counts", response_model=LibraryCountsResponse)
def get_library_counts(db: Session = Depends(get_db)):
    """
    Get aggregated counts from both Notes and Resources for the library page
    """
    # Get counts from Resources table
    resources = db.query(Resource).filter(Resource.is_active == True).all()
    notes_data = db.query(Note).all()
    
    # Resource counts by type
    slides_count = len([r for r in resources if r.type == 'slides'])
    videos_count = len([r for r in resources if r.type == 'videos'])
    books_count = len([r for r in resources if r.type == 'books'])
    
    # Resource counts by access type
    free_resources = len([r for r in resources if not r.is_premium])
    premium_resources = len([r for r in resources if r.is_premium])
    
    # Note counts
    total_notes = len(notes_data)
    free_notes = len([n for n in notes_data if n.access_type == 'free'])
    premium_notes = len([n for n in notes_data if n.access_type == 'premium'])
    
    # Total counts
    total_resources = len(resources) + total_notes
    
    return LibraryCountsResponse(
        notes_count=total_notes,
        slides_count=slides_count,
        videos_count=videos_count,
        books_count=books_count,
        total_resources=total_resources,
        free_resources=free_resources,
        premium_resources=premium_resources,
        total_notes=total_notes,
        free_notes=free_notes,
        premium_notes=premium_notes
    )

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """
    Get a specific note by ID
    """
    note = note_crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note: NoteCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_or_teacher)
):
    """
    Create a new note (admin or teacher only)
    """
    # Add uploaded_by field with current user's ID
    note_data = note.model_dump()
    note_data['uploaded_by'] = current_user.id
    
    return note_crud.create_note(db, note_data)

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int, 
    note_update: NoteUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_or_teacher)
):
    """
    Update a note (admin or teacher only)
    """
    updated_note = note_crud.update_note(db, note_id, note_update)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_or_teacher)
):
    """
    Delete a note (admin or teacher only)
    """
    success = note_crud.delete_note(db, note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return None
