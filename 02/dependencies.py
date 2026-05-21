from database import SessionLocal
from fastapi import Request

PROMPT_YAML_PATH = 'prompts.yaml'

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_httpx_client(request: Request):
    return request.app.state.http_client