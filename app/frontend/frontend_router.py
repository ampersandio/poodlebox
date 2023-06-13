from fastapi import APIRouter, Request, Form, HTTPException, File, UploadFile

from config import settings
from fastapi.templating import Jinja2Templates
from api.services.authorization import get_current_user, create_access_token, authenticate_user, verify_mail
from api.services.courses import get_course_by_id,get_students_courses, get_course_sections, get_nice_pending_enrollments
from api.services.users import get_user
from api.utils.utils import constants, file_upload

from jose import jwt
from api.utils.utils import user_registration_mail 
from mailjet_rest import Client

from api.data.models import StudentRegistration


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

    courses = get_courses(request, tag=tag)
    
    try:
        user = get_current_user(token)
        courses = get_courses(request, token, tag=tag)
    except:
        user = None
        courses = get_courses(request, tag=tag)

    if token:
        headers["authorization"] = f"Bearer {token}"

    popular_courses = requests.get(f"{host}/api/courses/popular", headers=headers)

    if tag:
        message = f"Courses tagged with {tag}"
    else:
        message = "Available Courses"

    return templates.TemplateResponse("index.html", {"request": request, "user": user, "courses": courses,  "most_popular": popular_courses.json(), "message":message} )


@frontend_router.get("/courses/{course_id}/enroll")
def enroll(request:Request, course_id:int):
    host = "http://" + request.headers["host"]
    token = request.cookies.get("token")
    headers = {}

    headers["authorization"] = f"Bearer {token}"
    payload = {'enroll': True}
    
    result = requests.put(f"{host}/api/students/courses/{course_id}", json=payload, headers=headers)

    if result.status_code == 201:
        return templates.TemplateResponse("message.html", {"request": request, "message": "Your request has been sent for review"})
    else:
        return templates.TemplateResponse("message.html", {"request": request, "message": "You're already enrolled in this course"})


@frontend_router.get("/profile")
def index(request: Request):
    token = request.cookies.get("token")
    host = "http://" + request.headers["host"]

    headers = {}

    try:
        user = get_current_user(token)
        courses = get_courses(request, token)
    except:
        user = None   

    if token:
        headers["authorization"] = f"Bearer {token}"

    popular_courses = requests.get(f"{host}/api/courses/popular", headers=headers)

    pending_courses = get_nice_pending_enrollments(user.id)
    
    if user.role == constants.TEACHER_ROLE:
        courses = [course for course in courses["items"] if course["teacher"]["email"] == user.email] 
    elif user.role == constants.STUDENT_ROLE:
        courses = get_students_courses(user.id)
    else:
        raise HTTPException(constants.COURSE_ACCESS_DENIED_DETAIL)
    

    return templates.TemplateResponse("profile.html", {"request": request, "user": user, "courses": courses,"most_popular": popular_courses.json(), "pending_enrollments":pending_courses} )


@frontend_router.post("/")
def form_data(request: Request, email: str = Form(...), password: str = Form(...)):
    user = authenticate_user(email, password)
    host = "http://" + request.headers["host"]
    headers = {}

    if user is not None:
        token = create_access_token({"sub": email})

        if token:
            headers["authorization"] = f"Bearer {token}"

        popular_courses = requests.get(f"{host}/api/courses/popular", headers=headers)
        courses = get_courses(request, token)
        
        response = templates.TemplateResponse("index.html",{"request": request, "user": user, "courses": courses, "headers": headers, "most_popular": popular_courses.json()})
        response.set_cookie(key="token", value=token)
        return response
    
    else:
        return templates.TemplateResponse("message.html", {"request": request, "message": "Login Invalid"})
    

@frontend_router.get("/courses/{course_id}/")
def course(request: Request,course_id:int):

    token = request.headers["cookie"][6:]

    user = get_current_user(token)
    course = get_course_by_id(course_id)
    sections = get_course_sections(course_id)
    student_courses = [course.id for course in get_students_courses(user.id)]

    return templates.TemplateResponse("course.html", {"request": request, "course":course, "sections":sections, "user":user, "student_courses":student_courses})


@frontend_router.get("/courses/{course_id}/sections/{section_id}")
def course(request: Request, course_id:int, section_id:int):
    host = "http://" + request.headers["host"]

    token = request.cookies.get("token")
    course = get_course_by_id(course_id)
    headers = {'Authorization': f'Bearer {token}'}
    try:

        user = get_current_user(token)
        section = requests.get(f"{host}/api/courses/{course_id}/sections/{section_id}", headers=headers)

    except:
        pass

    return templates.TemplateResponse("section.html", {"request": request, "user": user, "course":course, "section":section.json(), "host":host} )


@frontend_router.get("/search")
def search(request: Request, search_query: str):
    host = "http://"+(request.headers["host"])

    try:
        cookie_header = request.headers.get("cookie")[6:]
        user = get_current_user(cookie_header)

        courses = requests.get(f"{host}/api/courses?title={search_query}", headers={"authorization": f"Bearer {cookie_header}"})
        courses = courses.json()

        return templates.TemplateResponse("index.html", {"request": request, "user":user, "courses":courses})
    
    except:
        courses = requests.get(f"{host}/api/courses?title={search_query}")
        courses = courses.json()
        return templates.TemplateResponse("index.html", {"request": request, "courses":courses})


@frontend_router.get("/login")
def login(request:Request):
    return templates.TemplateResponse("login.html", {"request": request})


@frontend_router.get("/register")
def register(request:Request):
    return templates.TemplateResponse("register.html", {"request": request})


@frontend_router.post("/register")
def register(request: Request, email: str = Form(...), first_name: str = Form(...), last_name: str = Form(...),
             password: str = Form(...), date_of_birth: str = Form(...)):
    host = "http://" + request.headers["host"]

    # Prepare the request data
    data = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'password': password,
        'date_of_birth': date_of_birth
    }

    url = f'{host}/api/authorization/registration/students'
    response = requests.post(url, json=data)

    status_code = response.status_code

    student = StudentRegistration(email=email, first_name=first_name, last_name=last_name, password=password,
                                 date_of_birth=date_of_birth)


    if status_code == 201:
        return templates.TemplateResponse("message.html", {"request": request, "message":"Successfully Registered to Poodlebox!"})
    else:
        return templates.TemplateResponse("message.html", {"request": request, "message":"Something Went Wrong!"})


@frontend_router.get("/logout", tags=["Frontend"])
def logout(request: Request):

    response = templates.TemplateResponse("message.html", {"request": request, "message":"Successfully Logged Out!"})
    response.delete_cookie(key="token")
    return response


@frontend_router.post("/pending_enrollments")
def judge_enrollment(
    request: Request,
    user_id: int = Form(...),
    course_id: int = Form(...),
    approved: bool = Form(...),
):
    host = "http://" + request.headers["host"]
    token = request.cookies.get("token")
    headers = {}

    headers["authorization"] = f"Bearer {token}"
    payload = {'approved': approved,
               'user_id':user_id,
               'course_id':course_id
               }
    
    try:
        user = get_current_user(token)
        courses = get_courses(request, token)
    except:
        user = None
        courses = get_courses(request)

    if token:
        headers["authorization"] = f"Bearer {token}"

    pending_courses = get_nice_pending_enrollments(user.id)

    popular_courses = requests.get(f"{host}/api/courses/popular", headers=headers)
    
    result = requests.put(f"{host}/api/courses/pending_enrollments", data=payload, headers=headers) 


    if user.role == constants.TEACHER_ROLE:
        courses = [course for course in courses["items"] if course["teacher"]["email"] == user.email] 
    elif user.role == constants.STUDENT_ROLE:
        courses = get_students_courses(user.id)
    else:
        raise HTTPException(constants.COURSE_ACCESS_DENIED_DETAIL)
    

    if result.status_code == 200:
        return templates.TemplateResponse("profile.html", {"request": request, "user": user, "courses": courses,  "most_popular": popular_courses.json(),"pending_enrollments":pending_courses})
    else:
        return templates.TemplateResponse("message.html", {"request": request, "message": "Something Went Wrong"})


@frontend_router.post("/course_create")
def course_create(
 request: Request,
    title: str = Form(...),
    description: str = Form(...),
    objectives: str = Form(...),
    premium: bool = Form(None),
    price: float = Form(None),
    course_picture: UploadFile = File(None),
    tags: str = Form(...)
):

    token = request.cookies.get("token")
    headers = {}
    host = "http://" + request.headers["host"]

    headers["authorization"] = f"Bearer {token}"
    user = get_current_user(token)
    courses = get_courses(request, token)
    popular_courses = requests.get(f"{host}/api/courses/popular", headers=headers)
    pending_courses = get_nice_pending_enrollments(user.id)

    # print(popular_courses)
    # Form data as a dictionary
    form_data = {
        "title": title,
        "description": description,
        "objectives": objectives,
        "premium": premium,
        "price": price,
        "tags": tags,
    }

    courses = get_courses(request, token)
    
    if user.role == constants.TEACHER_ROLE:
        courses = [course for course in courses["items"] if course["teacher"]["email"] == user.email] 
    elif user.role == constants.STUDENT_ROLE:
        courses = get_students_courses(user.id)
    else:
        raise HTTPException(constants.COURSE_ACCESS_DENIED_DETAIL)
    
    file_upload(course_picture, "course_thumbnails", course)


    response = requests.post(host + "/api/teachers/courses", data=form_data, headers=headers)

    if response.status_code == 201:

        return templates.TemplateResponse("profile.html", {"request": request, "user":user, "courses":courses,"most_popular":popular_courses.json(), "pending_enrollments":pending_courses})
    else:
        return templates.TemplateResponse("message.html", {"request": request, "message": "Something Went Wrong"})



@frontend_router.get('/token/{token}', tags=['Authentication'])
def verify_token(request:Request, token:str):
    '''
    Endpoint to validate mail account.
    
    '''

    user = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    user = get_user(user["sub"])

    if user is not None:
        verify_mail(user)
        response = templates.TemplateResponse("message.html", {"request": request, "message":"Password Verified!"})
        return response
    else:
        response = templates.TemplateResponse("message.html", {"request": request, "message":"Verification Failed"})
        return response