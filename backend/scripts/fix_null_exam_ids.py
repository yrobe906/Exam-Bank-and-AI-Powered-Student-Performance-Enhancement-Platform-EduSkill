#!/usr/bin/env python3
\"\"\"One-time script to fix NULL exam_id in unlock_requests by matching exam_name.\"\"\"
import argparse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import engine  # Reuse project engine/DB config

def fix_null_exam_ids(dry_run: bool = True):
    db = SessionLocal()
    try:
        # Find corrupt requests
        corrupt = db.execute(text('''
            SELECT id, user_id, exam_name FROM unlock_requests 
            WHERE exam_id IS NULL AND exam_name IS NOT NULL AND status != 'deleted'
        ''')).fetchall()
        
        print(f"Found {len(corrupt)} corrupt requests:")
        for row in corrupt:
            print(f"  ID={row.id}, user={row.user_id}, exam_name='{row.exam_name}'")
        
        if dry_run:
            print("\\n[DRY-RUN] No changes applied. Use --execute to fix.")
            return
        
        fixed = 0
        for row in corrupt:
            req_id = row.id
            exam_name = row.exam_name
            exam = db.execute(
                text("SELECT id FROM exams WHERE name ILIKE :name LIMIT 1"),
                {&#x27;name&#x27;: exam_name}
            ).fetchone()
            
            if exam:
                db.execute(
                    text("UPDATE unlock_requests SET exam_id = :exam_id WHERE id = :req_id"),
                    {&#x27;exam_id&#x27;: exam[0], &#x27;req_id&#x27;: req_id}
                )
                fixed += 1
                print(f"  Fixed ID={req_id}: exam_id={exam[0]}")
            else:
                print(f"  SKIPPED ID={req_id}: No matching exam '{exam_name}'")
        
        db.commit()
        print(f"\n✅ Successfully fixed {fixed}/{len(corrupt)} requests.")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == &#x27;__main__&#x27;:
    parser = argparse.ArgumentParser(description="Fix NULL exam_id in unlock_requests")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Preview changes (default)")
    parser.add_argument("--execute", action="store_true", help="Apply changes to DB")
    args = parser.parse_args()
    
    fix_null_exam_ids(dry_run=not args.execute)

