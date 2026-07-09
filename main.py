from fastapi import FastAPI
from app.routers.router import router

app = FastAPI(title="Music card API")

app.include_router(router)