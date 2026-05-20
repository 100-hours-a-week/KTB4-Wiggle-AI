from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import schemas
import llm
import crud
from database import get_db, Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)


# posts/
@app.post("/posts", response_model=schemas.PostBase)
async def create_post(post: schemas.PostBase, db: Session = Depends(get_db)):
    re_post = crud.create_post_db(db, post)
    return JSONResponse(status_code=201, content=jsonable_encoder(re_post))

@app.get("/posts/{post_id}", response_model=schemas.PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    re_post = crud.read_post_db(db, post_id)
    return JSONResponse(status_code=200, content=jsonable_encoder(re_post))


@app.patch("/posts/{post_id}", response_model=schemas.PostResponse)
async def update_post(post_id:int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    re_post = crud.update_post_db(db, post_id, post)
    return JSONResponse(status_code=200, content=jsonable_encoder(re_post))

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int, post: schemas.PostDelete, db: Session = Depends(get_db)):
    re_post = crud.delete_post_db(db, post_id, post)
    return JSONResponse(status_code=200, content={})


# comments/
@app.post("/posts/{post_id}/comments/", response_model=schemas.CommentResponse)
async def create_comment(post_id:int, comment: schemas.CommentBase, db: Session = Depends(get_db)):
    re_comment = crud.create_comment_db(db, post_id, comment)
    return JSONResponse(status_code=201, content=jsonable_encoder(re_comment))

@app.patch("/comments/{comment_id}", response_model=schemas.CommentResponse)
async def update_comment(comment_id: int, comment: schemas.CommentUpdate, db: Session = Depends(get_db)):
    re_comment = crud.update_comment_db(db, comment_id, comment)
    return JSONResponse(status_code=200, content=jsonable_encoder(re_comment))

@app.delete("/comments/{comment_id}")
async def delete_comment(comment_id: int, comment: schemas.CommentDelete, db: Session = Depends(get_db)):
    re_comment = crud.delete_comment_db(db, comment_id, comment)
    return JSONResponse(status_code=200, content={})

@app.get("/comments/{comment_id}", response_model=schemas.CommentBase)
async def get_comment(comment_id: int, db: Session = Depends(get_db)):
    re_comment = crud.read_comment_db(db, comment_id)
    return JSONResponse(status_code=200, content=jsonable_encoder(re_comment))

# translates/
@app.get("/posts/{post_id}/translation/{target_language}")
async def translate_post(post_id: int, target_language: str = 'Korean', db: Session = Depends(get_db)):
    translated_post = llm.translate(db, post_id, target_language)
    return JSONResponse(status_code=200, content={'text': translated_post})

# summarize/
@app.get("/posts/{post_id}/summarization")
async def summarize_post(post_id: int, db: Session = Depends(get_db)):
    summarize_post = llm.summarize(db, post_id)
    return JSONResponse(status_code=200, content={'text': summarize_post})