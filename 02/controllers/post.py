from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas.post import PostCreate, PostDelete, PostUpdate
from models import PostModel
from .utils import check_id_existence, check_author_identity


def create_post_controller(db: Session, post: PostCreate):
    return PostModel.create_post(db, post)

def read_post_controller(db: Session, post_id: int):
    check_id_existence(db, PostModel, post_id)
    return PostModel.get_post_by_id(db, post_id)

def update_post_controller(db: Session, post_id: int, post:PostUpdate):
    check_id_existence(db, PostModel, post_id)
    check_author_identity(db, PostModel, post_id, post.author)
    return PostModel.update_post(db, post_id, post)

def delete_post_controller(db: Session, post_id: int, post: PostDelete):
    check_id_existence(db, PostModel, post_id)
    check_author_identity(db, PostModel, post_id, post.author)
    return PostModel.delete_post(db, post_id)