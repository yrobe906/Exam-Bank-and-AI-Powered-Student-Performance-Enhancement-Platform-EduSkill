from database import SessionLocal
import sqlalchemy as sa

db = SessionLocal()

# Add sector_name column to student_subject_analytics table
try:
    db.execute(sa.text("""
        ALTER TABLE student_subject_analytics 
        ADD COLUMN sector_name VARCHAR(150) DEFAULT 'Unknown'
    """))
    db.commit()
    print("Column sector_name added successfully!")
except Exception as e:
    print(f"Error: {e}")
    db.rollback()

db.close()
