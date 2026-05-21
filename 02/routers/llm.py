import httpx
from fastapi import Depends, APIRouter
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from dependencies import get_db, get_httpx_client
from controllers.llm import translate_stream_controller, summarize_stream_controller
from controllers.utils import check_id_existence
from models import PostModel

router = APIRouter(tags=['llm'])

@router.get("/posts/{post_id}/translation/{target_language}")
async def translate_post(post_id: int,
                   target_language: str = 'Korean',
                   db: Session = Depends(get_db),
                   client: httpx.AsyncClient = Depends(get_httpx_client)):
    check_id_existence(db, PostModel, post_id)

    async def response_generator():
        translate_stream = translate_stream_controller(client, db, post_id, target_language)
        async for chunk in translate_stream:
            yield chunk
    return StreamingResponse(response_generator(), media_type="text/event-stream")

@router.get("/posts/{post_id}/summarization")
async def summarize_post(post_id: int,
                         db: Session = Depends(get_db),
                         client: httpx.AsyncClient = Depends(get_httpx_client)):
    check_id_existence(db, PostModel, post_id)

    async def response_generator():
        summarize_stream = summarize_stream_controller(client, db, post_id)
        async for chunk in summarize_stream:
            yield chunk
    return StreamingResponse(response_generator(), media_type='text/event-stream')
