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

print("=== UNLOCK METHOD MIGRATION - Fix SQLAlchemy column error ===")

conn = psycopg2.connect(
    host=host,
    port=port,
    database=db,
    user=user,
    password=pass_
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

print("\n✓ Adding unlock_method column to student_exam_unlocks (CRITICAL FIX)")
cur.execute("""
ALTER TABLE student_exam_unlocks 
ADD COLUMN IF NOT EXISTS unlock_method VARCHAR(20) NOT NULL DEFAULT 'request';
""")

print("✅ SUCCESS: unlock_method column added/verified")
print("\nMigration complete! This fixes 'column student_exam_unlocks.unlock_method does not exist'")
print("🔄 Restart FastAPI: uvicorn main:app --reload")
print("🧪 Test: POST /api/admin/unlock/process/20")

cur.close()
conn.close()
print("Migration ready. Run: python add_unlock_method_migration.py")
