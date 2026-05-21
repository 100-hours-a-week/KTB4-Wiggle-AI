from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from schemas.post import PostCreate, PostDelete, PostResponse, PostUpdate
from dependencies import get_db
from controllers.post import (create_post_controller,
                              read_post_controller,
                              delete_post_controller,
                              update_post_controller,
                              read_post_list_controller)


router = APIRouter(tags=['posts'])

@router.post("/posts/", response_model=PostResponse)
def create_post(post: PostCreate,
                db: Session = Depends(get_db)):
    return create_post_controller(db, post)

@router.get("/posts/{post_id}", response_model=PostResponse)
def read_post(post_id: int,
                db: Session = Depends(get_db)):
    return read_post_controller(db, post_id)

@router.get("/posts/page/{page_idx}", response_model=List[PostResponse])
def read_post_list(page_idx: int, db: Session = Depends(get_db)):
    return read_post_list_controller(page_idx, db)

@router.patch("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int,
                   post: PostUpdate,
                   db: Session=Depends(get_db)):
    return update_post_controller(db, post_id, post)

@router.delete("/posts/{post_id}")
def delete_post(post_id: int,
                   post: PostDelete,
                   db: Session=Depends(get_db)):
    return delete_post_controller(db, post_id, post)