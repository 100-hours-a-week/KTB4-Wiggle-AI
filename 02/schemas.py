from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    text: str
    author: str

class PostUpdate(BaseModel):
    title: str
    text: str
    author: str
    
class PostResponse(BaseModel):
    id: int
    title: str
    text: str
    author: str
    upload_time: str

class PostDelete(BaseModel):
    author: str

class CommentBase(BaseModel):
    text: str
    author: str

class CommentResponse(BaseModel):
    id: int
    post_id: int
    text: str
    author: str
    upload_time: str

class CommentUpdate(BaseModel):
    text: str
    author: str
    
class CommentDelete(BaseModel):
    author: str