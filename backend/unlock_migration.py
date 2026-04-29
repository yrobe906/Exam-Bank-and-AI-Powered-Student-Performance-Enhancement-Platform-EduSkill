import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime

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

print("=== UNLOCK REQUESTS MIGRATION ===")

conn = psycopg2.connect(
    host=host,
    port=port,
    database=db,
    user=user,
    password=pass_
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

print("\n1. Adding exam_id column to unlock_requests if missing...")
cur.execute("""
ALTER TABLE unlock_requests 
ADD COLUMN IF NOT EXISTS exam_id INTEGER;
""")
print("- Added exam_id column")

print("\n2. Adding other missing columns...")
cur.execute("""
ALTER TABLE unlock_requests 
ADD COLUMN IF NOT EXISTS exam_name VARCHAR(200),
ADD COLUMN IF NOT EXISTS unlock_method VARCHAR(20),
ADD COLUMN IF NOT EXISTS points_required INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS price FLOAT DEFAULT 0.0,
ADD COLUMN IF NOT EXISTS payment_method VARCHAR(20),
ADD COLUMN IF NOT EXISTS payment_proof_path VARCHAR(500),
ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'pending',
ADD COLUMN IF NOT EXISTS payment_verified BOOLEAN DEFAULT false,
ADD COLUMN IF NOT EXISTS transaction_ref VARCHAR(100),
ADD COLUMN IF NOT EXISTS admin_notes VARCHAR(1000),
ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMP WITH TIME ZONE;
""")
print("- Added other columns")

print("\n3. Adding primary key if missing...")
cur.execute("""
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'unlock_requests_pkey') THEN
        ALTER TABLE unlock_requests ADD COLUMN IF NOT EXISTS id SERIAL;
        ALTER TABLE unlock_requests ADD CONSTRAINT unlock_requests_pkey PRIMARY KEY (id);
    END IF;
END $$;
""")
print("- Ensured primary key and id column")

print("\n4. Adding foreign keys...")
cur.execute("""
ALTER TABLE unlock_requests 
ADD CONSTRAINT IF NOT EXISTS fk_unlock_requests_user_id 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
""")
print("- Added user_id FK")

cur.execute("""
ALTER TABLE unlock_requests 
ADD CONSTRAINT IF NOT EXISTS fk_unlock_requests_exam_id 
FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE;
""")
print("- Added exam_id FK")

print("\n5. Adding indexes...")
cur.execute("CREATE INDEX IF NOT EXISTS idx_unlock_requests_status ON unlock_requests(status);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_unlock_requests_user_id ON unlock_requests(user_id);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_unlock_requests_exam_id ON unlock_requests(exam_id);")
print("- Added indexes")

print("\n6. Creating student_exam_unlocks table...")
cur.execute("""
CREATE TABLE IF NOT EXISTS student_exam_unlocks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    exam_id INTEGER NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
    unlocked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, exam_id)
);
CREATE INDEX IF NOT EXISTS idx_student_exam_unlocks_user_exam ON student_exam_unlocks(user_id, exam_id);
""")
print("- Created student_exam_unlocks table")

print("\n7. Populating exam_name for existing requests...")
cur.execute("""
UPDATE unlock_requests ur 
SET exam_name = COALESCE(ur.exam_name, e.name)
FROM exams e 
WHERE ur.exam_id = e.id 
AND ur.exam_name IS NULL OR ur.exam_name = '';
""")
print("- Populated exam_name")

print("\nMigration complete! /api/unlock/my-requests should now work.")

cur.close()
conn.close()

