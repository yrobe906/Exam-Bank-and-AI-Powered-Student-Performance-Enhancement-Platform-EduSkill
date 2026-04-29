"""
Migration script to add missing columns to unlock_requests table.
Run this script to fix the database schema mismatch.
"""
from database import SessionLocal
import sqlalchemy as sa

db = SessionLocal()

try:
    # Add payment_method column if it doesn't exist
    db.execute(sa.text("""
        ALTER TABLE unlock_requests 
        ADD COLUMN IF NOT EXISTS payment_method VARCHAR(50)
    """))
    print("✓ Column 'payment_method' added successfully!")
except Exception as e:
    print(f"Error adding payment_method column: {e}")
    db.rollback()

try:
    # Add transaction_reference column if it doesn't exist
    db.execute(sa.text("""
        ALTER TABLE unlock_requests 
        ADD COLUMN IF NOT EXISTS transaction_reference VARCHAR(100)
    """))
    print("✓ Column 'transaction_reference' added successfully!")
except Exception as e:
    print(f"Error adding transaction_reference column: {e}")
    db.rollback()

try:
    # Add payment_amount column if it doesn't exist
    db.execute(sa.text("""
        ALTER TABLE unlock_requests 
        ADD COLUMN IF NOT EXISTS payment_amount FLOAT
    """))
    print("✓ Column 'payment_amount' added successfully!")
except Exception as e:
    print(f"Error adding payment_amount column: {e}")
    db.rollback()

try:
    # Add payment_proof_url column if it doesn't exist
    db.execute(sa.text("""
        ALTER TABLE unlock_requests 
        ADD COLUMN IF NOT EXISTS payment_proof_url VARCHAR(255)
    """))
    print("✓ Column 'payment_proof_url' added successfully!")
except Exception as e:
    print(f"Error adding payment_proof_url column: {e}")
    db.rollback()

try:
    # Add payment_verified column if it doesn't exist
    db.execute(sa.text("""
        ALTER TABLE unlock_requests 
        ADD COLUMN IF NOT EXISTS payment_verified BOOLEAN DEFAULT FALSE
    """))
    print("✓ Column 'payment_verified' added successfully!")
except Exception as e:
    print(f"Error adding payment_verified column: {e}")
    db.rollback()

db.commit()
db.close()
print("\n✅ Migration completed! The unlock_requests table has been updated.")

