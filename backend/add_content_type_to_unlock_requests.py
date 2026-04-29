"""
Migration script to add content_type column to unlock_requests table.
Run this script to fix the database schema.
"""
from database import SessionLocal
import sqlalchemy as sa

db = SessionLocal()

try:
    # Add content_type column if it doesn't exist
    db.execute(sa.text("""
        ALTER TABLE unlock_requests 
        ADD COLUMN IF NOT EXISTS content_type VARCHAR(50) NOT NULL DEFAULT 'exam'
    """))
    print("✓ Column 'content_type' added successfully!")
except Exception as e:
    print(f"Error adding content_type column: {e}")
    db.rollback()

db.close()