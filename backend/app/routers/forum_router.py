from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.schemas.forum_schemas import (
    ForumPostCreate, 
    ForumPostResponse, 
    ForumCommentCreate, 
    ForumCommentResponse
)
from app.crud import forum_crud
from typing import List

router = APIRouter()

def get_current_user_id():
    """Get current user ID from localStorage (handled in frontend)"""
    pass

# Create a new post
@router.post("/posts", response_model=ForumPostResponse)
def create_post(post: ForumPostCreate, user_id: int, db: Session = Depends(get_db)):
    from app.models.user_models import User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    post_data = {
        "title": post.title,
        "content": post.content,
        "category": post.category
    }
    
    created_post = forum_crud.create_post(db, post_data, user_id)
    if not created_post:
        raise HTTPException(status_code=400, detail="Failed to create post")
    
    return created_post

# Get all posts with filtering
@router.get("/posts", response_model=List[dict])
def get_posts(
    filter_type: str = "latest",
    category: str = None,
    search: str = None,
    user_id: int = None,
    db: Session = Depends(get_db)
):
    posts = forum_crud.get_posts(db, user_id, filter_type, category, search)
    return posts

# Get a single post
@router.get("/posts/{post_id}", response_model=dict)
def get_post(post_id: int, user_id: int = None, db: Session = Depends(get_db)):
    post = forum_crud.get_post(db, post_id, user_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# Delete a post
@router.delete("/posts/{post_id}")
def delete_post(post_id: int, user_id: int, user_role: str, db: Session = Depends(get_db)):
    success = forum_crud.delete_post(db, post_id, user_id, user_role)
    if not success:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    return {"message": "Post deleted successfully"}

# Update a post (edit)
@router.put("/posts/{post_id}")
def update_post(post_id: int, post: ForumPostCreate, user_id: int, user_role: str, db: Session = Depends(get_db)):
    post_data = {
        "title": post.title,
        "content": post.content,
        "category": post.category
    }
    updated_post = forum_crud.update_post(db, post_id, user_id, user_role, post_data)
    if not updated_post:
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")
    return updated_post

# Toggle like on a post
@router.post("/posts/{post_id}/like")
def toggle_like(post_id: int, user_id: int, db: Session = Depends(get_db)):
    result = forum_crud.toggle_like(db, post_id, user_id)
    if result[0] is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"likes_count": result[0], "is_liked": result[1]}

# Toggle bookmark on a post
@router.post("/posts/{post_id}/bookmark")
def toggle_bookmark(post_id: int, user_id: int, db: Session = Depends(get_db)):
    result = forum_crud.toggle_bookmark(db, post_id, user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"is_bookmarked": result}

# Pin/Unpin a post (teacher or admin only)
@router.post("/posts/{post_id}/pin")
def toggle_pin(post_id: int, is_pinned: bool, user_role: str, db: Session = Depends(get_db)):
    if user_role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Only teachers or admin can pin posts")
    
    post = forum_crud.toggle_pin(db, post_id, is_pinned)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post pinned successfully", "is_pinned": is_pinned}

# Get comments for a post
@router.get("/posts/{post_id}/comments", response_model=List[ForumCommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    comments = forum_crud.get_comments(db, post_id)
    return comments

# Create a comment
@router.post("/posts/{post_id}/comments", response_model=ForumCommentResponse)
def create_comment(post_id: int, comment: ForumCommentCreate, user_id: int, user_role: str = "student", db: Session = Depends(get_db)):
    created_comment = forum_crud.create_comment(db, post_id, user_id, comment.content, user_role)
    if not created_comment:
        raise HTTPException(status_code=400, detail="Failed to create comment")
    return created_comment

# Get bookmarked posts
@router.get("/bookmarks", response_model=List[dict])
def get_bookmarks(user_id: int, db: Session = Depends(get_db)):
    posts = forum_crud.get_bookmarked_posts(db, user_id)
    return posts
