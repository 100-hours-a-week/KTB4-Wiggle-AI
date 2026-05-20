import yaml
import requests
from crud import read_post_db
from sqlalchemy.orm import Session

PROMPT_PATH = './prompts.yaml'
with open(PROMPT_PATH, 'r', encoding="utf-8") as f:
    prompts = yaml.safe_load(f)

def translate(db: Session, post_id: int, target_language: str):
    post = read_post_db(db, post_id)
    title = post.title
    text = post.text

    url = prompts['url']
    cfg = prompts['translate']
    payload = {
        "model": cfg['model'],
        "stream": False,
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
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result['message']['content']
    except requests.exceptions.RequestException as e:
        return f"[Local LLM Error] 요청 실패: {str(e)}"

def summarize(db: Session, post_id: int):
    post = read_post_db(db, post_id)
    text = post.text

    url = prompts['url']
    cfg = prompts['summarize']
    payload = {
        'model': cfg['model'],
        'stream': False,
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
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result['message']['content']
    except requests.exceptions.RequestException as e:
        return f"[Local LLM Error] 요청 실패: {str(e)}"