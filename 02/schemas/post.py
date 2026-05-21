from typing import List
from pydantic import BaseModel
from datetime import datetime
from schemas.comment import CommentResponse

class PostCreate(BaseModel):
    title: str
    text: str
    author: str

class PostUpdate(BaseModel):
    title: str
    text: str
    author: str

class PostDelete(BaseModel):
    author: str
    
class PostResponse(BaseModel):
    id: int
    title: str
    text: str
    author: str
    comment: List[CommentResponse]
    upload_time: datetime