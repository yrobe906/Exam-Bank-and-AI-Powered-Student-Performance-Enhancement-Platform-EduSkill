import hashlib
import os
from typing import Union
from passlib.context import CryptContext

SALT_SIZE = 32
HASH_ITERATIONS = 600000
DIGEST = "sha256"

# Support both bcrypt (legacy DB users) and PBKDF2 (new registrations)
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 (default), supports bcrypt fallback."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against any supported hash format (bcrypt or PBKDF2)."""
    return pwd_context.verify(plain_password, hashed_password)

