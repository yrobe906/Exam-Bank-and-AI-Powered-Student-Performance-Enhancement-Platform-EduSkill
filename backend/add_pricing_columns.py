"""
Add pricing columns to the exams table
Run this script to add pricing_type and amount columns to existing databases
"""
import sys
sys.path.insert(0, '.')

from database import engine, Base
from sqlalchemy import text

def add_pricing_columns():
    """Add pricing columns to exams table"""
    with engine.connect() as conn:
        # Check if columns exist
        result = conn.execute(text("PRAGMA table_info(exams)"))
        columns = [row[1] for row in result]
        
        if 'pricing_type' not in columns:
            conn.execute(text("ALTER TABLE exams ADD COLUMN pricing_type VARCHAR(20) DEFAULT 'Free'"))
            print("Added pricing_type column")
        
        if 'amount' not in columns:
            conn.execute(text("ALTER TABLE exams ADD COLUMN amount FLOAT DEFAULT 0"))
            print("Added amount column")
        
        conn.commit()
        print("Database updated successfully!")

if __name__ == "__main__":
    add_pricing_columns()
