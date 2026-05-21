from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas.comment import CommentCreate, CommentDelete, CommentUpdate
from models import PostModel, CommentModel
from .utils import check_id_existence, check_author_identity


def create_comment_controller(db: Session, post_id: int, comment: CommentCreate):
    check_id_existence(db, PostModel, post_id)
    return CommentModel.create_comment(db, post_id, comment)

def read_comment_controller(db: Session, comment_id: int):
    check_id_existence(db, CommentModel, comment_id)
    return CommentModel.get_comment_by_id(db, comment_id)

def update_comment_controller(db: Session, comment_id: int, comment:CommentUpdate):
    check_id_existence(db, CommentModel, comment_id)
    check_author_identity(db, CommentModel, comment_id, comment.author)
    return CommentModel.update_comment(db, comment_id, comment)

def delete_comment_controller(db: Session, comment_id: int, comment: CommentDelete):
    check_id_existence(db, CommentModel, comment_id)
    check_author_identity(db, CommentModel, comment_id, comment.author)
    return CommentModel.delete_comment(db, comment_id)