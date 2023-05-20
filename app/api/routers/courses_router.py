from fastapi import APIRouter, Depends, HTTPException, Response, Header, Request
from fastapi.responses import JSONResponse
from typing import Annotated, Optional
from api.services import courses
from api.data.models import User, CourseCreate
from api.services.authorization import get_current_user
from api.services.students import get_students_courses_id

courses_router = APIRouter(prefix="/courses")


@courses_router.get("/")
def get_all_courses(
    request: Request,
    token: str = Header(None),
    title=None,
    tag=None,
    sort=None,
    sort_by=None,
):
    if "authorization" not in request.headers.keys() and token is None:
        result = courses.get_courses_anonymous()
    elif token is not None and get_current_user(token).role == "student":
        result = courses.get_courses_student(get_current_user(token).id)
    elif token is not None and get_current_user(token).role == "teacher":
        result = courses.get_courses_teacher()
    elif (
        "authorization" in request.headers.keys()
        and get_current_user(request.headers.get("authorization")[7:]).role == "student"
    ):
        result = courses.get_courses_student(
            get_current_user(request.headers.get("authorization")[7:]).id
        )
    elif (
        "authorization" in request.headers.keys()
        and get_current_user(request.headers.get("authorization")[7:]).role == "teacher"
    ):
        result = courses.get_courses_teacher()
    else:
        raise HTTPException(status_code=401, detail="User not authenticated")
    if title:
        result = [x for x in result if title.lower() in x.title.lower()]
    if tag:
        result = [x for x in result if tag in x.tags]

    if sort and (sort == "asc" or sort == "desc"):
        if sort_by == "id":
            result = sorted(result, key=lambda r: r.id, reverse=sort == "desc")
        elif sort_by == "rating":
            result = sorted(result, key=lambda r: r.rating, reverse=sort == "desc")

    return result


@courses_router.get("/{course_id}")
def get_course_by_id(
    course_id, current_user: Annotated[User, Depends(get_current_user)]
):
    result = courses.get_course_by_id(course_id)
    if result == "Not found":
        raise HTTPException(status_code=404, detail="Course not found")
    if (
        current_user.role == "Student"
        and result.id not in get_students_courses_id(current_user.id)
        and result.premium is True
    ):
        raise HTTPException(
            status_code=402, detail="You don't have access to this course"
        )
    return result


@courses_router.put("/")
def create_course(course: CourseCreate, current_user: User = Depends(get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403, detail="You don't have access to this section"
        )
    course_result=courses.get_course_by_title(course.title)
    if course_result!="Not found":
        raise HTTPException(
            status_code=400, detail="A course with that title already exists"
        )     
    if current_user.verified_email == False:
        raise HTTPException(status_code=403, detail="Your email is not verified")
    new_course=courses.create_course(course, current_user.id)
    if new_course!=None:
        raise HTTPException(
            status_code=400, detail=new_course
        )   
    return JSONResponse(status_code=201, content={"msg":"Course created"})
