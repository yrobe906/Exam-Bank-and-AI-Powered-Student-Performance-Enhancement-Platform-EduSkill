import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Upload settings
UPLOAD_BASE = BASE_DIR / "uploads"
UPLOAD_FOLDERS = {
    "notes": UPLOAD_BASE / "Notes",
    "slides": UPLOAD_BASE / "Slides",
    "videos": UPLOAD_BASE / "Videos", 
    "books": UPLOAD_BASE / "Books"
}
PREVIEW_FOLDER = UPLOAD_BASE / "Previews"

# Create directories
for folder in UPLOAD_FOLDERS.values():
    folder.mkdir(parents=True, exist_ok=True)
PREVIEW_FOLDER.mkdir(parents=True, exist_ok=True)

# File settings
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB