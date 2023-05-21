from fastapi import APIRouter, Request,  Form
from config import settings
from fastapi.templating import Jinja2Templates
from api.services.authorization import get_current_user, create_access_token, authenticate_user
from api.utils.utils import generate_html 
from mailjet_rest import Client


import requests

frontend_router = APIRouter(include_in_schema=False, prefix="/poodlebox")
templates = Jinja2Templates(directory="frontend/templates")

mailjet = Client(auth=(settings.api_key, settings.api_secret), version='v3.1')


def get_courses(request: Request, token: str = None):
    host = "http://" + request.headers["host"]
    headers = {}

    if token:
        headers["AuThoRizaTion"] = f"Bearer {token}"

    courses = requests.get(f"{host}/api/courses", headers=headers)
    return courses.json()


@frontend_router.get("/")
def index(request: Request):
    host = "http://" + request.headers["host"]
    try:
        token = request.headers.get("cookie")[6:]
        user = get_current_user(token)
        courses = get_courses(request, token)

    except:
        user = None
        courses = get_courses(request)

    popular_courses = requests.get(f"{host}/api/courses/popular")
    print(popular_courses.json())
    return templates.TemplateResponse("index.html", {"request": request, "user": user, "courses": courses, "most_popular":popular_courses.json()})

@frontend_router.get("/search")
def search(request: Request, search_query: str):
    host = "http://"+(request.headers["host"])

    try:
        cookie_header = request.headers.get("cookie")[6:]
        user = get_current_user(cookie_header)

        courses = requests.get(f"{host}/api/courses?title={search_query}", headers={"AuThoRizaTion": f"Bearer {cookie_header}"})
        courses = courses.json()

        return templates.TemplateResponse("index.html", {"request": request, "user":user, "courses":courses})
    
    except:
        courses = requests.get(f"{host}/api/courses?title={search_query}")
        return templates.TemplateResponse("index.html", {"request": request, "courses":courses.json()})


@frontend_router.get("/login")
def login(request:Request):
    return templates.TemplateResponse("login.html", {"request": request})


@frontend_router.get("/register")
def register(request:Request):
    return templates.TemplateResponse("register.html", {"request": request})

@frontend_router.post("/register")
def register(
        request:Request, 
        username: str = Form(...),
        password: str = Form(...),
        email: str = Form(...),
        date_of_birth:str = Form(...)):
    
    host = "http://" + request.headers["host"]
    data = generate_html(username,host)
    result = mailjet.send.create(data=data)

    print (result.status_code)
    print (result.json())

    return templates.TemplateResponse("message.html", {"request": request})


@frontend_router.post("/")
def process_form_data(request: Request, username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)

    if user is not None:
        token = create_access_token({"sub": username})
        courses = get_courses(request, token)
        response = templates.TemplateResponse("index.html", {"request": request, "user": user, "courses": courses})
        response.set_cookie(key="token", value=token)
        return response
    else:
        return templates.TemplateResponse("message.html", {"request": request, "message": "Login Invalid"})


@frontend_router.get("/logout", tags=["Frontend"])
def logout(request: Request):

    response = templates.TemplateResponse("message.html", {"request": request, "message":"Successfully Logged Out!"})
    response.delete_cookie(key="token")
    return response
