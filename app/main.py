from functools import lru_cache

from fastapi import FastAPI
from config import Settings
from api.api_router import api_router
from frontend.frontend_router import frontend_router

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

app = FastAPI()

app.include_router(api_router)
app.include_router(frontend_router)

@app.get("/")
def index():
    return "hello"