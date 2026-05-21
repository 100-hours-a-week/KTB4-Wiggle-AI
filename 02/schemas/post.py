from pydantic import BaseModel
from datetime import datetime

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
    upload_time: datetime