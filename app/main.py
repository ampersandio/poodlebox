from functools import lru_cache
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI, Request
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
app.mount("/static", StaticFiles(directory="frontend/style"), name="static")
app.mount("/assets", StaticFiles(directory="assets/course_thumbnails"), name="assets")


@app.middleware("http")
async def create_auth_header(request: Request, call_next,):
    '''
    Check if there are cookies set for authorization. If so, construct the
    Authorization header and modify the request (unless the header already
    exists!)
    '''

    if ("Authorization" not in request.headers and "Authorization" in request.cookies):

        access_token = request.cookies["Authorization"]

        request.headers.__dict__["_list"].append(
            ( "authorization".encode(), f"Bearer {access_token}".encode(),))
    
    response = await call_next(request)
    return response    
