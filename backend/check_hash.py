# check_hash.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hash_from_db = "$2b$12$S3AeJqo6b1fLmNcXzVpYBO9k7rT2wQ1uH4vP6sY8dC0lM5nG7iKjL"
password = "admin2149"

is_valid = pwd_context.verify(password, hash_from_db)
print(f"Hash verification: {is_valid}")

if not is_valid:
    print("❌ Hash doesn't match password 'admin2149'")
    print("Generate new hash:")
    new_hash = pwd_context.hash("admin2149")
    print(f"New hash: {new_hash}")
else:
    print("✅ Hash matches password")