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

conn = psycopg2.connect(
    host=host,
    port=port,
    database=db,
    user=user,
    password=pass_
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

print("Adding missing columns to users table if not exist...")

cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS xp_points INTEGER DEFAULT 0;")
print("- Added xp_points")

cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS current_tier VARCHAR(20) DEFAULT 'bronze';")
print("- Added current_tier")

cur.execute("""
CREATE TABLE IF NOT EXISTS admin_unlock_requests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    username VARCHAR NOT NULL,
    full_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    user_xp INTEGER DEFAULT 0,
    user_tier VARCHAR(20) DEFAULT 'bronze',
    user_streak INTEGER DEFAULT 0,
    content_type VARCHAR NOT NULL,
    content_id INTEGER NOT NULL,
    content_title VARCHAR NOT NULL,
    unlock_method VARCHAR(20) DEFAULT 'payment',
    points_used INTEGER DEFAULT 0,
    price FLOAT DEFAULT 0.0,
    payment_method VARCHAR(20),
    transaction_ref VARCHAR(100),
    request_reason TEXT,
    status VARCHAR DEFAULT 'pending',
    payment_proof_path VARCHAR,
    admin_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE,
    processed_by INTEGER
);
""")
print("- Created admin_unlock_requests table")

cur.execute("""
CREATE TABLE IF NOT EXISTS user_premium_access (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    content_type VARCHAR NOT NULL,
    content_id INTEGER NOT NULL,
    access_granted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    granted_by INTEGER,
    payment_method VARCHAR
);
""")
print("- Created user_premium_access table")

# Ensure admin_unlock_requests table contains the expected new fields
cur.execute("ALTER TABLE admin_unlock_requests ADD COLUMN IF NOT EXISTS user_xp INTEGER DEFAULT 0;")
cur.execute("ALTER TABLE admin_unlock_requests ADD COLUMN IF NOT EXISTS user_tier VARCHAR(20) DEFAULT 'bronze';")
cur.execute("ALTER TABLE admin_unlock_requests ADD COLUMN IF NOT EXISTS user_streak INTEGER DEFAULT 0;")
cur.execute("ALTER TABLE admin_unlock_requests ADD COLUMN IF NOT EXISTS unlock_method VARCHAR(20) DEFAULT 'payment';")
cur.execute("ALTER TABLE admin_unlock_requests ADD COLUMN IF NOT EXISTS points_used INTEGER DEFAULT 0;")
cur.execute("ALTER TABLE admin_unlock_requests ADD COLUMN IF NOT EXISTS price FLOAT DEFAULT 0.0;")
cur.execute("ALTER TABLE admin_unlock_requests ADD COLUMN IF NOT EXISTS payment_method VARCHAR(20);")
cur.execute("ALTER TABLE admin_unlock_requests ADD COLUMN IF NOT EXISTS transaction_ref VARCHAR(100);")
print("- Ensured admin_unlock_requests has the new admin fields")

print("=== UNLOCK REQUESTS MIGRATION ===")

# Add unlock_requests table columns and constraints if missing
print("\nAdding unlock_requests table structure...")

# Add exam_id column if missing
cur.execute("""
ALTER TABLE unlock_requests 
ADD COLUMN IF NOT EXISTS exam_id INTEGER,
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
print("- Added missing columns to unlock_requests")

# Add primary key if missing
cur.execute("""
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'unlock_requests_pkey') THEN
        ALTER TABLE unlock_requests ADD CONSTRAINT unlock_requests_pkey PRIMARY KEY (id);
    END IF;
END $$;
""")
print("- Ensured primary key")

# Add foreign keys if missing
cur.execute("""
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'fk_unlock_requests_user_id'
    ) THEN
        ALTER TABLE unlock_requests ADD CONSTRAINT fk_unlock_requests_user_id
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
    END IF;
END
$$;
""")
print("- Added user_id FK")

cur.execute("""
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'fk_unlock_requests_exam_id'
    ) THEN
        ALTER TABLE unlock_requests ADD CONSTRAINT fk_unlock_requests_exam_id
        FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE;
    END IF;
END
$$;
""")
print("- Added exam_id FK")

# Create index on status and user_id for queries
cur.execute("CREATE INDEX IF NOT EXISTS idx_unlock_requests_status ON unlock_requests(status);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_unlock_requests_user_id ON unlock_requests(user_id);")
print("- Added indexes")

# Create student_exam_unlocks table if missing
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

# Data migration: Update existing requests with exam_name (if exam_id was somehow populated, or skip if no data)
cur.execute("""
UPDATE unlock_requests ur 
SET exam_name = e.name
FROM exams e 
WHERE ur.exam_id = e.id 
AND ur.exam_name IS NULL;
""")
print("- Populated exam_name for existing requests")

cur.close()
conn.close()

print("DB migration complete. The /api/unlock/my-requests endpoint should now work. Restart server and test.")
