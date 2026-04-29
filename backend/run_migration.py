"""
Run migration to add pricing columns to exams table
"""
import sys
sys.path.insert(0, '.')

from database import engine
from sqlalchemy import text

def run_migration():
    """Add pricing columns to exams table"""
    with engine.connect() as conn:
        # Add pricing_type column
        try:
            conn.execute(text("""
                ALTER TABLE exams ADD COLUMN pricing_type VARCHAR(20) DEFAULT 'Free'
            """))
            print("Added pricing_type column")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("pricing_type column already exists")
            else:
                print(f"Error adding pricing_type: {e}")
        
        # Add amount column
        try:
            conn.execute(text("""
                ALTER TABLE exams ADD COLUMN amount FLOAT DEFAULT 0
            """))
            print("Added amount column")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("amount column already exists")
            else:
                print(f"Error adding amount: {e}")
        
        conn.commit()
        
        # Verify columns
        result = conn.execute(text("""
            SELECT column_name, data_type, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'exams' 
            AND column_name IN ('pricing_type', 'amount')
        """))
        print("\nVerified columns:")
        for row in result:
            print(f"  {row[0]}: {row[1]} default={row[2]}")

if __name__ == "__main__":
    run_migration()
