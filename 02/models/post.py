from database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, Session
from schemas.post import PostCreate, PostUpdate, PostDelete
from datetime import datetime


N_POST_PER_PAGE = 5

class PostModel(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    text = Column(String)
    author = Column(String, index=True)
    upload_time = Column(DateTime)

    comment = relationship(
        "CommentModel", 
        back_populates="post", 
        cascade="all, delete-orphan"
    )

    @classmethod
    def is_id_exists(cls, db: Session, target_id: int):
        if db.query(cls.id).filter(cls.id==target_id).first():
            return True
        else:
            return False
        
    @classmethod
    def get_author_by_id(cls, db: Session, target_id:int):
        return db.query(cls.author).filter(cls.id==target_id).first()

    @classmethod
    def create_post(cls, db: Session, post: PostCreate):
        db_post = cls(
            title = post.title,
            text = post.text,
            author = post.author,
            upload_time = datetime.now()
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post

    @classmethod
    def get_post_by_id(cls, db: Session, post_id: int):
        return  db.query(cls).filter(cls.id==post_id).first()
    
    @classmethod
    def read_post_list(cls, page_idx: int, db: Session):
        if page_idx < 1:
            page_idx = 1
        return db.query(cls).offset((page_idx-1) * N_POST_PER_PAGE).limit(N_POST_PER_PAGE).all()

    @classmethod
    def update_post(cls, db: Session, post_id: int, post: PostUpdate):
        db_post = cls.get_post_by_id(db, post_id)
        db_post.text = post.text
        db.commit()
        db.refresh(db_post)
        return db_post

    @classmethod
    def delete_post(cls, db: Session, post_id: int):
        db_post = cls.get_post_by_id(db, post_id)
        db.delete(db_post)
        db.commit()
        return True
        
