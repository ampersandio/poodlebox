from functools import lru_cache
from fastapi.staticfiles import StaticFiles
import uvicorn

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from config import Settings
from api.api_router import api_router
from frontend.frontend_router import frontend_router
import uvicorn

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

app = FastAPI()
add_pagination(app)


app.include_router(api_router)
app.include_router(frontend_router)
app.mount("/static", StaticFiles(directory="frontend/style"), name="static")
app.mount("/assets", StaticFiles(directory="assets/course_thumbnails"), name="assets")

