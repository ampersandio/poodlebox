from functools import lru_cache

from fastapi import FastAPI
from config import Settings
from routers.authorization import authorization_router


@lru_cache
def get_settings() -> Settings:
    return Settings()
settings = get_settings()

app = FastAPI()

app.include_router(authorization_router)