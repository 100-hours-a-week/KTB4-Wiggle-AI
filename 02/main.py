import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import Base, engine
from routers.comment import router as comment_router
from routers.post import router as post_router
from routers.llm import router as llm_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(timeout=60)
    Base.metadata.create_all(bind=engine)
    yield
    await app.state.http_client.aclose()


app = FastAPI(lifespan=lifespan)


app.include_router(post_router)
app.include_router(comment_router)
app.include_router(llm_router)