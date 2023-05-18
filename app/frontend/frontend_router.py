from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

frontend_router = APIRouter(include_in_schema=False,prefix="/poodlebox")

templates = Jinja2Templates(directory="frontend/templates")


@frontend_router.get("/")
def index(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})

@frontend_router.get("/login")
def login(request:Request):
    return templates.TemplateResponse("login.html", {"request": request})


@frontend_router.get("/register")
def register(request:Request):
    return templates.TemplateResponse("register.html", {"request": request})

