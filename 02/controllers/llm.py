import json
import yaml
import httpx
from sqlalchemy.orm import Session
from models import PostModel
from dependencies import PROMPT_YAML_PATH

with open(PROMPT_YAML_PATH, 'r', encoding="utf-8") as f:
    prompts = yaml.safe_load(f)

def format_sse_data(content: str):
    safe_content = content.replace('\n', '\\n')
    return f"data: {safe_content}\n\n"

async def translate_stream_controller(client: httpx.AsyncClient,
                                db: Session,
                                post_id: int,
                                target_language: str):
    post = PostModel.get_post_by_id(db, post_id)
    title = post.title
    text = post.text

    url = prompts['url']
    cfg = prompts['translate']
    payload = {
        "model": cfg['model'],
        "stream": True,
        "messages": [{
            "role":"system",
            "content": cfg["prompt"]['system'],
        },
        {
            "role": 'user',
            "content": cfg['prompt']['user'].format(target_language=target_language,
                                                    title=title,
                                                    text=text
                                                    )
        }]
    }
    headers = {"Content-Type": "application/json"}

    try:
        async with client.stream("POST", url, json=payload, headers=headers) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                data = json.loads(line)
                content = data.get('message', {}).get('content', {})
                if content:
                    yield format_sse_data(content)
                
                if data.get('done', False):
                    break
    except (httpx.HTTPError, json.JSONDecodeError) as exc:
        yield format_sse_data(f"LLM error: {exc}")
    return

async def summarize_stream_controller(client: httpx.AsyncClient, db: Session, post_id: int):
    post = PostModel.get_post_by_id(db, post_id)
    text = post.text

    url = prompts['url']
    cfg = prompts['summarize']
    payload = {
        'model': cfg['model'],
        'stream': True,
        "messages": [{
            "role":"system",
            "content": cfg["prompt"]['system'],
        },
        {
            "role": 'user',
            "content": cfg['prompt']['user'].format(text=text)
        }]
    }
    headers = {"Content-Type": "application/json"}

    try:
        async with client.stream("POST", url, json=payload, headers=headers) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                data = json.loads(line)
                content = data.get('message', {}).get('content', {})
                if content:
                    yield format_sse_data(content)
                
                if data.get('done', False):
                    break
    except (httpx.HTTPError, json.JSONDecodeError) as exc:
        yield format_sse_data(f"LLM error: {exc}")
    return
