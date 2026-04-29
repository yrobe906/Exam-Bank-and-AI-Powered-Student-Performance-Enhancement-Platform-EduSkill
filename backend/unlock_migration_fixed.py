import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv()

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:4316@localhost:5432/register_db")

# Parse URL
if 'postgresql://' in DB_URL:
    user_pass, host_port_db = DB_URL.split('@')
    user, pass_ = user_pass.replace('postgresql://', '').split(':')
    host_port, db = host_port_db.split('/')
    host, port = host_port.split(':')
else:
    raise ValueError("Invalid DB_URL")

print("=== FINAL UNLOCK FIX MIGRATION (exam_id column only) ===")

conn = psycopg2.connect(
    host=host,
    port=port,
    database=db,
    user=user,
    password=pass_
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

print("\n✓ VERIFIED: Adding exam_id column (CRITICAL FIX for SQLAlchemy error)")
cur.execute("""
ALTER TABLE unlock_requests 
ADD COLUMN IF NOT EXISTS exam_id INTEGER;
""")
print("SUCCESS: exam_id column added/verified")

print("\nMigration complete! This fixes the 'column unlock_requests.exam_id does not exist' error.")
print("Restart your FastAPI server and test GET /api/unlock/my-requests")

cur.close()
conn.close()
print("Ready for testing.")

