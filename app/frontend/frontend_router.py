from fastapi import APIRouter, Request, Depends, Form, HTTPException
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from api.data.models import User
from api.services.authorization import get_current_user, create_access_token, authenticate_user

import requests


frontend_router = APIRouter(include_in_schema=False,prefix="/poodlebox")

templates = Jinja2Templates(directory="frontend/templates")


@frontend_router.get("/")
def index(request:Request):
    host = "http://"+(request.headers["host"])
    try:
        cookie_header = request.headers.get("cookie")[6:]
        user = get_current_user(cookie_header)
        
        courses = requests.get(f"{host}/api/courses", headers={"AuThoRizaTion": f"Bearer {cookie_header}"})
        courses = courses.json()


        return templates.TemplateResponse("index.html", {"request": request, "user":user, "courses":courses})
    
    except:

        courses = requests.get(f"{host}/api/courses")
        return templates.TemplateResponse("index.html", {"request": request, "courses":courses.json()})


@frontend_router.get("/login")
def login(request:Request):
    return templates.TemplateResponse("login.html", {"request": request})


@frontend_router.get("/register")
def register(request:Request):
    return templates.TemplateResponse("register.html", {"request": request})


@frontend_router.post("/")
def process_form_data(request:Request, username: str = Form(...), password: str = Form(...), ):
    host = (request.headers["host"])

    user = authenticate_user(username,password)

    if user is not None:
        token = create_access_token({"sub":username})

    user = get_current_user(token)

    if user is not None:

        courses = requests.get(f"{host}/api/courses", headers={"AuThoRizaTion": f"Bearer {token}"})
        response = templates.TemplateResponse("index.html", {"request": request, "user": user, "courses":courses.json()})
        response.set_cookie(key="token", value=token)


        return response
    
    else:
        return templates.TemplateResponse("message.html", {"request": request, "message": "Login Invalid"})
    

@frontend_router.get("/logout", tags=["Frontend"])
def logout(request: Request):

    response = templates.TemplateResponse("message.html", {"request": request, "message":"Successfully Logged Out!"})
    response.delete_cookie(key="token")
    return response
