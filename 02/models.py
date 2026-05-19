from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    text = Column(String)
    author = Column(String, index=True)
    upload_time = Column(DateTime)
    pass

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    author = Column(String, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    upload_time = Column(DateTime)
    pass