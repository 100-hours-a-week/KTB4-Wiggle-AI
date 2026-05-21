from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship, Session
from schemas.comment import CommentCreate, CommentUpdate, CommentDelete

class CommentModel(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    author = Column(String, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    post = relationship("PostModel", back_populates="comment")
    upload_time = Column(DateTime)

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
    def create_comment(cls, db: Session, post_id: int, comment: CommentCreate):
        db_comment = cls(
            text = comment.text,
            author = comment.author,
            post_id = post_id,
            upload_time = datetime.now()
        )
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    @classmethod
    def get_comment_by_id(cls, db: Session, comment_id: int):
        return db.query(cls).filter(cls.id==comment_id).first()
    
    @classmethod
    def update_comment(cls, db: Session, comment_id: int, comment: CommentUpdate):
        db_comment = cls.get_comment_by_id(db, comment_id)
        db_comment.text = comment.text
        db.commit()
        db.refresh(db_comment)
        return db_comment

    @classmethod
    def delete_comment(cls, db: Session, comment_id: int):
        db_comment = cls.get_comment_by_id(db, comment_id)
        db.delete(db_comment)
        db.commit()
        return True