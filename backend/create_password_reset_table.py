#!/usr/bin/env python3
"""
Migration script to create password_reset_tokens table
Run this script to add the password reset functionality to your database.
"""

from database import engine, Base
from app.models.password_reset_models import PasswordResetToken

def create_password_reset_table():
    """Create the password_reset_tokens table"""
    try:
        print("Creating password_reset_tokens table...")
        Base.metadata.create_all(bind=engine, tables=[PasswordResetToken.__table__])
        print("Successfully created password_reset_tokens table")
    except Exception as e:
        print(f"Error creating table: {e}")

if __name__ == "__main__":
    create_password_reset_table()