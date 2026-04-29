"""
Migration script to add the missing 'rating' column to section_feedback table.
Run this script to fix the database schema.
"""
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:4316@localhost:5432/register_db"
)

def add_rating_column():
    """Add the rating column to section_feedback table if it doesn't exist"""
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Check if column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'section_feedback' AND column_name = 'rating'
        """))
        
        if result.fetchone() is None:
            # Add the column
            conn.execute(text("""
                ALTER TABLE section_feedback 
                ADD COLUMN rating INTEGER
            """))
            conn.commit()
            print("✅ Successfully added 'rating' column to section_feedback table")
        else:
            print("ℹ️  'rating' column already exists in section_feedback table")
        
        # Also check and add other columns that might be missing
        columns_to_check = [
            ('rating', 'INTEGER'),
            ('status', 'VARCHAR(20) DEFAULT \'pending\''),
            ('internal_notes', 'TEXT'),
            ('updated_at', 'TIMESTAMP'),
        ]
        
        for col_name, col_type in columns_to_check:
            result = conn.execute(text(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'section_feedback' AND column_name = '{col_name}'
            """))
            
            if result.fetchone() is None:
                conn.execute(text(f"""
                    ALTER TABLE section_feedback 
                    ADD COLUMN {col_name} {col_type}
                """))
                conn.commit()
                print(f"✅ Successfully added '{col_name}' column to section_feedback table")
            else:
                print(f"ℹ️  '{col_name}' column already exists in section_feedback table")

if __name__ == "__main__":
    add_rating_column()
    print("\n✅ Migration completed successfully!")

