from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from datetime import datetime
import schemas
from models import Post, Comment
from sqlalchemy.orm import Session

def check_author_identity(user, author) -> bool:
    if user != author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit/delete your own posts/comments"
        )
    else:
        return True
    
def check_post_existence(db: Session, post_id: int) -> bool:
    if db.query(Post.id).filter(Post.id == post_id).first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return True

def check_comment_existence(db: Session, comment_id: int) -> bool:
    if db.query(Comment.id).filter(Post.id == comment_id).first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return True



# Post
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

def read_post_db(db: Session, post_id: int) -> Post:
    check_post_existence(db, post_id)
    db_post = db.query(Post).filter(Post.id==post_id).options(selectinload(Post.comment)).first()
    return db_post

def update_post_db(db: Session, post_id: int, post: schemas.PostUpdate) -> Post:
    check_post_existence(db, post_id)
    db_post = db.query(Post).filter(Post.id == post_id).first()
    check_author_identity(post.author, db_post.author)
    db_post.title = post.title
    db_post.text = post.text
    
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post_db(db: Session, post_id: int, post: schemas.PostDelete) -> None:
    check_post_existence(db, post_id)
    db_post = db.query(Post).filter(Post.id==post_id).first()
    check_author_identity(post.author, db_post.author)
    db.delete(db_post)
    db.commit()
    return True

# Comment
def create_comment_db(db: Session, post_id:int, comment: schemas.CommentBase) -> Comment:
    check_post_existence(db, post_id)
    db_comment = Comment(
        post_id = post_id,
        text = comment.text,
        author = comment.author,
        upload_time = datetime.now()
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def read_comment_db(db: Session, comment_id: int):
    check_comment_existence(db, comment_id)
    db_comment = db.query(Comment).filter(Comment.id==comment_id).first()
    return db_comment

def update_comment_db(db: Session, comment_id: int, comment: schemas.CommentUpdate) -> Comment:
    check_comment_existence(db, comment_id)
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    check_author_identity(comment.author, db_comment.author)
    db_comment.text = comment.text
    
    db.commit()
    db.refresh(db_comment)
    return db_comment
    
def delete_comment_db(db: Session, comment_id:int, comment: schemas.CommentDelete) -> Comment:
    check_comment_existence(db, comment_id)
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    check_author_identity(comment.author, db_comment.author)
    db.delete(db_comment)
    db.commit()
    return True
