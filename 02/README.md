# Week 02 - Community Board API

> KTB 위클리 챌린지 2주차 — FastAPI 기반 커뮤니티 게시판 서버

---

## How to Use

```bash
uv sync
```

```bash
uvicorn main:app
```
```bash
streamlit run streamlit_app.py
```
---

## API Endpoints


### Posts

| 메서드 | 경로 | 설명 |
|---|---|---|
| GET | `/posts/{post_id}` | 단일 게시글 조회 |
| GET | `/posts/page/{page_idx}` | 게시글 목록 조회  |
| POST | `/posts` | 게시글 작성 |
| PATCH | `/posts/{idx}` | 게시글 수정 |
| DELETE | `/posts/{idx}` | 게시글 삭제 |

### Comments

| 메서드 | 경로 | 설명 |
|---|---|---|
| GET | `/comments/{comment_id}` | 단일 게시글 조회 |
| POST | `/posts/{idx}/comments` | 댓글 작성 |
| PUT | `/comments/{comment_id}` | 댓글 수정 |
| DELETE | `/comments/{comment_id}` | 댓글 삭제 |

### LLM Summarization / Translation

| 메서드 | 경로 | 설명 |
|---|---|---|
| GET | `/posts/{post_id}/translation/{target_language}` | LLM 게시글 번역 (스트리밍 출력)|
| GET | `/posts/{post_id}/summarization` | LLM 게시글 요약 (스트리밍 출력) |

---

## 회고
웹을 정말 오랜만에 다뤄봐서 그동안 까먹은 내용이 정말 많았다.
Pydantic, ORM(SQLAlchemy), httpx 모두 처음 사용해봤고, 두 굉장히 강력한 도구들이라는 게 느껴졌다.
이전에 딥러닝 모델을 배포할 때는 DB작업을 모두 백엔드 맡겨 파이썬 코드로 DB를 다뤄본 적이 없었는데, 이번 기회에 파이썬 ORM으로 DB를 간단하게나마 다뤄볼 수 있어 좋았다. 

또, 과거에 stable diffusion 모델을 서빙할 때, 생성시간이 너무 길어 스트리밍 출력으로 이를 보완하고자 했지만 일정이 촉박해 포기한 적이 있었다. 아쉬움이 많이 남았어서 이번에는 꼭 구현하자 다짐했었고, 새벽까지 매달려 httpx를 사용한 스트리밍 출력 기능까지 추가한 점이 만족스럽다. 다음에 LLM이 아닌 diffusion과 같은 모델에도 충분히 적용할 수 있을 것 같다.

마지막에 추가 과제를 통해 router, controller, model로 나누어 코드를 리팩토링하는 작업도 상당히 재밌었다. 디자인 패턴이니 같은 단어를 들어는 봤었지만 이해도 바로 안 되고, 내 코드에 적용해본 적은 없었다. 경력이 있으신 jungjin이나 steve의 코드를 참고하면서 많이 배웠고, 직접 구현해보고 나니 경로, 내부 로직, DB와 관련된 기능들을 왜, 어떻게 분리시키는지 이해가 됐다.

<details>
<summary><b>260518</b></summary>
- API 설계
- Pydantic 스키마와 SQLAlchemy 모델 클래스 구현
- 게시글 기능 일부 구현
</details>

<details>
<summary><b>260519</b></summary>
- 게시글, 댓글 CRUD 구현
- 예외처리 추가
</details>

<details>
<summary><b>260520</b></summary>
- 로컬 LLM을 통한 번역, 요약 기능 추가
- HTTPX를 활용한 스트리밍 출력 기능 추가
</details>

<details>
<summary><b>260520</b></summary>
- LLM, 스트리밍 출력 기능 마무리
- Router, Controller, Model로 코드 리팩토링
- 마무리
</details>