#!/usr/bin/env python3
"""
Migration script to create or update the announcements table.
Run this after updating the models.
"""

from database import engine, Base
from app.models.announcement_models import Announcement
from sqlalchemy import text

def create_or_update_announcements_table():
    """Create or update the announcements table."""
    try:
        print("Creating/updating announcements table...")

        # Create table if it doesn't exist
        Announcement.__table__.create(engine, checkfirst=True)

        # Check if new columns exist, add them if they don't
        with engine.connect() as conn:
            # Check for file_path column
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name = 'announcements' AND column_name = 'file_path'
            """))
            if not result.fetchone():
                print("Adding file_path column...")
                conn.execute(text("ALTER TABLE announcements ADD COLUMN file_path VARCHAR(500)"))
                conn.commit()

            # Check for file_name column
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name = 'announcements' AND column_name = 'file_name'
            """))
            if not result.fetchone():
                print("Adding file_name column...")
                conn.execute(text("ALTER TABLE announcements ADD COLUMN file_name VARCHAR(255)"))
                conn.commit()

        print("✅ Announcements table updated successfully!")
    except Exception as e:
        print(f"❌ Error updating announcements table: {e}")

if __name__ == "__main__":
    create_or_update_announcements_table()