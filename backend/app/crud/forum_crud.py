from sqlalchemy.orm import Session
from app.models.forum_models import ForumPost, ForumPostLike, ForumComment, ForumBookmark
from app.models.user_models import User
from app.models.admin import Admin
from sqlalchemy import desc, func
from typing import List, Optional

# Create a new forum post
def create_post(db: Session, post_data: dict, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    
    post = ForumPost(
        title=post_data["title"],
        content=post_data["content"],
        category=post_data["category"],
        user_id=user_id,
        username=user.username,
        user_role=user.role,
        profile_image=user.profile_photo if user.profile_photo else None
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# Get all posts with optional filtering
def get_posts(db: Session, current_user_id: int, filter_type: str = "latest", category: str = None, search: str = None):
    query = db.query(ForumPost).filter(ForumPost.is_approved == True)
    
    # Apply search filter
    if search:
        query = query.filter(
            (ForumPost.title.ilike(f"%{search}%")) | 
            (ForumPost.content.ilike(f"%{search}%")) |
            (ForumPost.username.ilike(f"%{search}%"))
        )
    
    # Apply category filter
    if category:
        query = query.filter(ForumPost.category == category)
    
    # Apply sorting
    if filter_type == "latest":
        query = query.order_by(desc(ForumPost.created_at))
    elif filter_type == "unanswered":
        query = query.outerjoin(ForumComment).group_by(ForumPost.id).having(func.count(ForumComment.id) == 0)
        query = query.order_by(desc(ForumPost.created_at))
    elif filter_type == "most_liked":
        query = query.outerjoin(ForumPostLike).group_by(ForumPost.id).order_by(desc(func.count(ForumPostLike.id)))
    elif filter_type == "pinned":
        query = query.order_by(ForumPost.is_pinned.desc(), desc(ForumPost.created_at))
    
    posts = query.all()
    
    # Process posts with like count, comment count, and user's like status
    result = []
    for post in posts:
        likes_count = db.query(ForumPostLike).filter(ForumPostLike.post_id == post.id).count()
        comments_count = db.query(ForumComment).filter(ForumComment.post_id == post.id).count()
        is_liked = db.query(ForumPostLike).filter(
            ForumPostLike.post_id == post.id,
            ForumPostLike.user_id == current_user_id
        ).first() is not None
        is_bookmarked = db.query(ForumBookmark).filter(
            ForumBookmark.post_id == post.id,
            ForumBookmark.user_id == current_user_id
        ).first() is not None
        
        post_dict = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "category": post.category,
            "user_id": post.user_id,
            "username": post.username,
            "user_role": post.user_role,
            "profile_image": post.profile_image,
            "is_pinned": post.is_pinned,
            "is_approved": post.is_approved,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "likes_count": comments_count,  # Display comments count as likes
            "comments_count": comments_count,
            "is_liked": is_liked,
            "is_bookmarked": is_bookmarked
        }
        result.append(post_dict)
    
    return result

# Get a single post by ID
def get_post(db: Session, post_id: int, current_user_id: int):
    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not post:
        return None
    
    likes_count = db.query(ForumPostLike).filter(ForumPostLike.post_id == post.id).count()
    comments_count = db.query(ForumComment).filter(ForumComment.post_id == post.id).count()
    is_liked = db.query(ForumPostLike).filter(
        ForumPostLike.post_id == post.id,
        ForumPostLike.user_id == current_user_id
    ).first() is not None
    is_bookmarked = db.query(ForumBookmark).filter(
        ForumBookmark.post_id == post.id,
        ForumBookmark.user_id == current_user_id
    ).first() is not None
    
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "category": post.category,
        "user_id": post.user_id,
        "username": post.username,
        "user_role": post.user_role,
        "profile_image": post.profile_image,
        "is_pinned": post.is_pinned,
        "is_approved": post.is_approved,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "likes_count": comments_count,  # Display comments count as likes
        "comments_count": comments_count,
        "is_liked": is_liked,
        "is_bookmarked": is_bookmarked
    }

# Delete a post (only by owner, teacher, or admin)
def delete_post(db: Session, post_id: int, user_id: int, user_role: str):
    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not post:
        return False
    
    # Check if user is admin first (admin role can delete any post)
    if user_role == "admin":
        # Admin can delete any post
        db.delete(post)
        db.commit()
        return True
    
    # Allow deletion if user is owner or teacher
    if post.user_id != user_id and user_role not in ["teacher"]:
        return False
    
    db.delete(post)
    db.commit()
    return True

# Update a post (only by owner, teacher, or admin)
def update_post(db: Session, post_id: int, user_id: int, user_role: str, post_data: dict):
    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not post:
        return None
    
    # Check if user is admin first (admin role can edit any post)
    if user_role == "admin":
        # Admin can edit any post
        post.title = post_data.get("title", post.title)
        post.content = post_data.get("content", post.content)
        post.category = post_data.get("category", post.category)
        db.commit()
        db.refresh(post)
        return post
    
    # Allow edit if user is owner or teacher
    if post.user_id != user_id and user_role not in ["teacher"]:
        return None
    
    post.title = post_data.get("title", post.title)
    post.content = post_data.get("content", post.content)
    post.category = post_data.get("category", post.category)
    
    db.commit()
    db.refresh(post)
    return post

# Toggle like on a post
def toggle_like(db: Session, post_id: int, user_id: int):
    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not post:
        return None, False
    
    existing_like = db.query(ForumPostLike).filter(
        ForumPostLike.post_id == post_id,
        ForumPostLike.user_id == user_id
    ).first()
    
    if existing_like:
        db.delete(existing_like)
        db.commit()
        is_liked = False
    else:
        new_like = ForumPostLike(post_id=post_id, user_id=user_id)
        db.add(new_like)
        db.commit()
        is_liked = True
    
    likes_count = db.query(ForumPostLike).filter(ForumPostLike.post_id == post_id).count()
    comments_count = db.query(ForumComment).filter(ForumComment.post_id == post_id).count()
    return comments_count, is_liked  # Return comments_count as likes_count for display

# Toggle bookmark on a post
def toggle_bookmark(db: Session, post_id: int, user_id: int):
    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not post:
        return None, False
    
    existing_bookmark = db.query(ForumBookmark).filter(
        ForumBookmark.post_id == post_id,
        ForumBookmark.user_id == user_id
    ).first()
    
    if existing_bookmark:
        db.delete(existing_bookmark)
        db.commit()
        is_bookmarked = False
    else:
        new_bookmark = ForumBookmark(post_id=post_id, user_id=user_id)
        db.add(new_bookmark)
        db.commit()
        is_bookmarked = True
    
    return is_bookmarked

# Pin/Unpin a post (teacher or admin)
def toggle_pin(db: Session, post_id: int, is_pinned: bool):
    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not post:
        return None
    
    post.is_pinned = is_pinned
    db.commit()
    db.refresh(post)
    return post

# Get comments for a post
def get_comments(db: Session, post_id: int):
    comments = db.query(ForumComment).filter(ForumComment.post_id == post_id).order_by(desc(ForumComment.created_at)).all()
    return comments

# Create a comment
def create_comment(db: Session, post_id: int, user_id: int, content: str, user_role: str = "student", username: str = "Admin", profile_image: str = None):
    # Check if user is admin
    if user_role == "admin":
        admin = db.query(Admin).filter(Admin.id == user_id).first()
        if admin:
            username = admin.username
            profile_image = None
        else:
            # Fallback to User table
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            username = user.username
            profile_image = user.profile_photo
    else:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        username = user.username
        profile_image = user.profile_photo
    
    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not post:
        return None
    
    comment = ForumComment(
        post_id=post_id,
        user_id=user_id,
        username=username,
        user_role=user_role,
        profile_image=profile_image,
        content=content
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

# Get user's bookmarked posts
def get_bookmarked_posts(db: Session, user_id: int):
    bookmarks = db.query(ForumBookmark).filter(ForumBookmark.user_id == user_id).all()
    post_ids = [b.post_id for b in bookmarks]
    posts = db.query(ForumPost).filter(ForumPost.id.in_(post_ids)).all()
    
    result = []
    for post in posts:
        likes_count = db.query(ForumPostLike).filter(ForumPostLike.post_id == post.id).count()
        comments_count = db.query(ForumComment).filter(ForumComment.post_id == post.id).count()
        
        result.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "category": post.category,
            "user_id": post.user_id,
            "username": post.username,
            "user_role": post.user_role,
            "profile_image": post.profile_image,
            "is_pinned": post.is_pinned,
            "is_approved": post.is_approved,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "likes_count": likes_count,
            "comments_count": comments_count,
            "is_liked": False,
            "is_bookmarked": True
        })
    
    return result
