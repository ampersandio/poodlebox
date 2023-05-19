from fastapi import APIRouter, Request, Depends
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from api.data.models import User
from api.services.authorization import get_current_user
import requests


frontend_router = APIRouter(include_in_schema=False,prefix="/poodlebox")

templates = Jinja2Templates(directory="frontend/templates")


@frontend_router.get("/")
def index(request:Request):
    print(request)
    courses = requests.get("http://localhost:8002/api/authorization/test")
    print(courses.json())
    return templates.TemplateResponse("index.html", {"request": request})

@frontend_router.get("/login")
def login(request:Request):
    return templates.TemplateResponse("login.html", {"request": request})


@frontend_router.get("/register")
def register(request:Request):
    return templates.TemplateResponse("register.html", {"request": request})

