
from fastapi import APIRouter, Depends, HTTPException, Response, Header, Request
from typing import Annotated, Optional
from api.services import courses
from api.data.models import User
from api.services.authorization import get_current_user

courses_router = APIRouter(prefix="/courses")


@courses_router.get("/")
def get_all_courses(request:Request,title=None,tag=None,sort=None,sort_by=None):
    if "Authorization" not in request.headers.keys():
        result=courses.get_courses_anonymous()
    elif "Authorization" in request.headers.keys() is not None and get_current_user(request.headers.get("Authorization")[7:]).role=="Student":
        result=courses.get_course_by_id(get_current_user(request.headers.get("Authorization")[7:]).id)
    elif "Authorization" in request.headers.keys() is not None and get_current_user(request.headers.get("Authorization")[7:]).role=="Teacher":
       result=courses.get_courses_teacher()
    else:
       raise HTTPException(status_code=401,detail="User not authenticated")
    if title:
       result=[x for x in result if title.lower() in x.title.lower()]
    if tag:
       result=[x for x in result if tag in x.tags]
             
    if sort and (sort == 'asc' or sort == 'desc'):
        if sort_by=="id":
         result=sorted(result, key=lambda r:r.id,reverse=sort=="desc")
        elif sort_by=="rating":
          result=sorted(result, key=lambda r:r.rating,reverse=sort=="desc")
    
    return result
        

@courses_router.get("/{course_id}")
def get_course_by_id(course_id,current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.role=="Student" and result.id not in current_user.access and result.premium is True:
        raise  HTTPException(status_code=402,detail="You don't have access to this course")
    result=courses.get_course_by_id(course_id)
    if result=='Not found':
        raise HTTPException(status_code=404,detail="Course not found")
    return result
