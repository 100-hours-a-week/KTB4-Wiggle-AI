from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from schemas.comment import CommentCreate, CommentDelete, CommentResponse, CommentUpdate
from dependencies import get_db
from controllers.comment import create_comment_controller, read_comment_controller, update_comment_controller, delete_comment_controller


router = APIRouter(tags=['comments'])

@router.post("/posts/{post_id}/comments", response_model=CommentResponse)
def create_comment(post_id: int,
                comment: CommentCreate,
                db: Session = Depends(get_db)):
    return create_comment_controller(db, post_id, comment)

@router.get("/comments/{comment_id}", response_model=CommentResponse)
def read_comment(comment_id: int,
                db: Session = Depends(get_db)):
    return read_comment_controller(db, comment_id)

@router.patch("/comments/{comment_id}", response_model=CommentResponse)
def update_comment(comment_id: int,
                   comment: CommentUpdate,
                   db: Session=Depends(get_db)):
    return update_comment_controller(db, comment_id, comment)

@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int,
                   comment: CommentDelete,
                   db: Session=Depends(get_db)):
    return delete_comment_controller(db, comment_id, comment)