import sqlite3
print('=== DATABASE CHECK ===')
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Tables
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print('Tables:', [row[0] for row in c.fetchall()])

# Exams
print('\\n=== EXAMS ===')
c.execute('PRAGMA table_info(exams)')
print('Exams schema:', c.fetchall())
c.execute('SELECT id,name,pricing_type,amount FROM exams LIMIT 5')
print('Sample exams:', c.fetchall())
c.execute('SELECT COUNT(*) FROM exams WHERE pricing_type=?', ('Premium',))
print('Premium exams count:', c.fetchone()[0])

# Users
print('\\n=== USERS ===')
c.execute('PRAGMA table_info(users)')
print('Users schema:', [col[1] for col in c.fetchall()])
c.execute('SELECT id,full_name,xp_points FROM users WHERE role=? LIMIT 3', ('student',))
print('Sample students:', c.fetchall())

# Unlocks
print('\\n=== UNLOCK TABLES ===')
for table in ['unlock_requests', 'student_exam_unlocks']:
    try:
        c.execute(f'SELECT COUNT(*) FROM {table}')
        print(f'{table}:', c.fetchone()[0])
        c.execute(f'SELECT * FROM {table} LIMIT 1')
        row = c.fetchone()
        print(f'Sample {table}:', row)
    except:
        print(f'{table}: missing')

conn.close()
print('\\nRun: python check_db.py → paste output!')

