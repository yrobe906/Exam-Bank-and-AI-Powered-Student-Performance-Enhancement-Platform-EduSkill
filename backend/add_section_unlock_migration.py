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

print("=== ADD SECTION SUPPORT TO UNLOCK_REQUESTS MIGRATION ===")

conn = psycopg2.connect(
    host=host,
    port=port,
    database=db,
    user=user,
    password=pass_
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

print("\n1. Adding section_id column to unlock_requests")
cur.execute("""
ALTER TABLE unlock_requests 
ADD COLUMN IF NOT EXISTS section_id INTEGER;
""")
print("✓ section_id column added/verified")

print("\n2. Adding pricing_type column to unlock_requests")
cur.execute("""
ALTER TABLE unlock_requests 
ADD COLUMN IF NOT EXISTS pricing_type VARCHAR(20);
""")
print("✓ pricing_type column added/verified")

print("\n3. Adding indexes for performance")
cur.execute("""
CREATE INDEX IF NOT EXISTS idx_unlock_requests_section_user 
ON unlock_requests (user_id, section_id) WHERE section_id IS NOT NULL;
""")
print("✓ Indexes created")

print("\nMigration complete! Ready for model updates.")
print("Next: Update app/models/unlock_models_fixed.py and restart FastAPI.")

cur.close()
conn.close()
print("Migration ready. Run: python add_section_unlock_migration.py")

