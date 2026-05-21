from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    text: str
    author: str

class CommentResponse(BaseModel):
    id: int
    post_id: int
    text: str
    author: str
    upload_time: datetime

class CommentUpdate(BaseModel):
    text: str
    author: str
    
class CommentDelete(BaseModel):
    author: str