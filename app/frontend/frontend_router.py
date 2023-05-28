from fastapi import APIRouter, Request,  Form, Depends
from config import settings
from fastapi.templating import Jinja2Templates
from api.services.authorization import get_current_user, create_access_token, authenticate_user
from api.services.courses import get_course_by_id,get_students_courses
from api.utils.utils import user_registration 
from mailjet_rest import Client


import requests

frontend_router = APIRouter(include_in_schema=False, prefix="/poodlebox")
templates = Jinja2Templates(directory="frontend/templates")

mailjet = Client(auth=(settings.api_key, settings.api_secret), version='v3.1')


def get_courses(request: Request, token: str | None  = None, tag:str = None):
    host = "http://" + request.headers["host"]
    headers = {}

    if token:
        headers["authorization"] = f"Bearer {token}"
    
    if tag:
        courses = requests.get(f"{host}/api/courses/?tag={tag}", headers=headers)
    else:
        courses = requests.get(f"{host}/api/courses/", headers=headers)

    return courses.json()


@frontend_router.get("/")
def index(request: Request,tag:str=None):
    host = "http://" + request.headers["host"]
    headers = {}
    
    token = request.cookies.get("token")

    try:
        user = get_current_user(token)
        courses = get_courses(request, token, tag=tag)
    except:
        user = None
        courses = get_courses(request, tag=tag)

    if token:
        headers["authorization"] = f"Bearer {token}"

    # user_courses_ids = get_students_courses(user.id)
    # print(user.id)
    # print(user_courses_ids)
    # print([item["id"] for item in courses])

    popular_courses = requests.get(f"{host}/api/courses/popular", headers=headers)

    return templates.TemplateResponse("index.html", {"request": request, "user": user, "courses": courses,  "most_popular": popular_courses.json()} )


@frontend_router.post("/")
def form_data(request: Request, username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)
    host = "http://" + request.headers["host"]
    headers = {}

    if user is not None:
        token = create_access_token({"sub": username})

        if token:
            headers["authorization"] = f"Bearer {token}"
        popular_courses = requests.get(f"{host}/api/courses/popular", headers=headers)

        courses = get_courses(request, token)
        response = templates.TemplateResponse(
            "index.html",
            {"request": request, "user": user, "courses": courses, "headers": headers, "most_popular": popular_courses.json()}
        )
        response.set_cookie(key="token", value=token)
        return response
    else:
        return templates.TemplateResponse("message.html", {"request": request, "message": "Login Invalid"})
    

@frontend_router.get("/courses/{course_id}/")
def course(request: Request,course_id:int):

    token = request.headers["cookie"][6:]

    user = get_current_user(token)
    course = get_course_by_id(course_id)

    return templates.TemplateResponse("course.html", {"request": request, "course":course, "user":user})


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
    data = user_registration(username,host)
    result = mailjet.send.create(data=data)

    print (result.status_code)
    print (result.json())

    return templates.TemplateResponse("message.html", {"request": request})


@frontend_router.get("/logout", tags=["Frontend"])
def logout(request: Request):

    response = templates.TemplateResponse("message.html", {"request": request, "message":"Successfully Logged Out!"})
    response.delete_cookie(key="token")
    return response
