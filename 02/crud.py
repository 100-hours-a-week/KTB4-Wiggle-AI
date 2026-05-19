from fastapi import HTTPException, status
from datetime import datetime
import schemas
from models import Post
from utils import check_author_identity

from sqlalchemy.orm import Session
def create_post_db(db: Session, post: schemas.PostBase) -> Post:
    db_post = Post(
        title = post.title,
        text = post.text,
        author = post.author,
        upload_time = datetime.now()
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post_db(db: Session, post: schemas.PostUpdate) -> Post:
    db_post = db.query(Post).filter(Post.id == post.id).first()
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    check_author_identity(post.author, db_post.author)
    db_post.title = post.title
    db_post.text = post.text
    
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post_db(db: Session, post: schemas.PostDelete) -> None:
    db_post = db.query(Post).filter(Post.id==post.id).first()
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    check_author_identity(post.author, db_post.author)
    db.delete(db_post)
    db.commit()
    return True

def read_post_db(db: Session, post: schemas.PostGet) -> Post:
    db_post = db.query(Post).filter(Post.id==post.id).first()
    return db_post

def create_comment_db():
    return

def update_comment_db():
    return

def delete_comment_db():
    return

def get_comment_db():
    return