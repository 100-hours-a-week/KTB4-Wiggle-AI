from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import schemas
from models import Post, Comment
from database import get_db, Base, engine
import crud

app = FastAPI()
Base.metadata.create_all(bind=engine)



@app.post("/posts", response_model=schemas.PostBase)
async def create_post(post: schemas.PostBase, db: Session = Depends(get_db)):
    re_post = crud.create_post_db(db, post)
    return JSONResponse(status_code=201, content=jsonable_encoder(re_post))

@app.get("/posts", response_model=schemas.PostResponse)
async def get_post(post: schemas.PostGet, db: Session = Depends(get_db)):
    re_post = crud.read_post_db(db, post)
    return JSONResponse(status_code=200, content=jsonable_encoder(re_post))

@app.patch("/posts", response_model=schemas.PostResponse)
async def update_post(post: schemas.PostUpdate, db: Session = Depends(get_db)):
    re_post = crud.update_post_db(db, post)
    return JSONResponse(status_code=200, content=jsonable_encoder(re_post))

@app.delete("/posts")
async def delete_post(post: schemas.PostDelete, db: Session = Depends(get_db)):
    re_post = crud.delete_post_db(db, post)
    return JSONResponse(status_code=200, content={})

@app.post("/comments/", response_model=schemas.CommentBase)
async def create_comment(comment: schemas.CommentBase):
    print(comment)
    return JSONResponse(status_code=201, content=comment.model_dump())



