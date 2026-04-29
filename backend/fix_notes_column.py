from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Check if column exists first
    result = conn.execute(text("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name = 'notes' AND column_name = 'uploaded_by'
    """))
    if not result.fetchone():
        conn.execute(text('ALTER TABLE notes ADD COLUMN uploaded_by INTEGER'))
        conn.commit()
        print('Column added successfully')
    else:
        print('Column already exists')

