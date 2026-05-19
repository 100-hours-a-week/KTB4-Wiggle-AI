from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    text: str
    author: str

class PostUpdate(PostBase):
    id: int
    
class PostResponse(PostBase):
    id: int
    upload_time: str

class PostGet(BaseModel):
    id: int

class PostDelete(BaseModel):
    id: int
    author: str


class CommentBase(BaseModel):
    post_id: int
    text: str
    author: str

class CommentResponse(CommentBase):
    id: int
    upload_time: str

class CommentUpdate(CommentBase):
    id: int
