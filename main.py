from fastapi import FastAPI
from app.routers.router import router
from contextlib import asynccontextmanager
from redis_client import redis_pool

@asynccontextmanager
async def lifespan(app):
    yield
    redis_pool.disconnect()

app = FastAPI(title="Music card API", lifespan=lifespan)

app.include_router(router)