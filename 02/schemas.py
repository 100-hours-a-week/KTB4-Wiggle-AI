from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    text: str
    author: str

class PostUpdate(BaseModel):
    id: int
    title: str
    text: str
    author: str
    
class PostResponse(BaseModel):
    id: int
    title: str
    text: str
    author: str
    upload_time: str

class PostRead(BaseModel):
    id: int

class PostDelete(BaseModel):
    id: int
    author: str


class CommentBase(BaseModel):
    post_id: int
    text: str
    author: str

class CommentResponse(BaseModel):
    id: int
    post_id: int
    text: str
    author: str
    upload_time: str

class CommentUpdate(BaseModel):
    id: int
    text: str
    author: str
    
class CommentDelete(BaseModel):
    id: int
    author: str

class CommentRead(BaseModel):
    id: int