
from fastapi import APIRouter, Depends, HTTPException, Response, Header, Request
from typing import Annotated, Optional
from api.services import courses
from api.data.models import User
from api.services.authorization import get_current_user
from api.services.courses import get_students_courses, get_student_course_by_id, get_course_by_id

students_router = APIRouter(prefix="/students")



@students_router.get("/courses")
def get_courses_for_student(current_user:User=Depends(get_current_user),sort=None,sort_by=None,title=None,subscription=None):
    result=get_students_courses(current_user)
    if title:
       result=[x for x in result if title.lower() in x.title.lower()]
    if subscription:
       result=[x for x in result if subscription.lower() in x.subscription.lower()]
    if sort and (sort == 'asc' or sort == 'desc'):
        if sort_by=="id":
         result=sorted(result, key=lambda r:r.id,reverse=sort=="desc")
        elif sort_by=="rating":
          result=sorted(result, key=lambda r:r.rating,reverse=sort=="desc")
        elif sort_by=='progress':
          result=sorted(result, key=lambda r:r.progress,reverse=sort=="desc")           

@students_router.get("/courses/{course_id}")
def get_course_for_student_by_id(course_id,current_user:User=Depends(get_current_user)):
    if get_course_by_id(course_id)=='Not found':
        raise HTTPException(status_code=404,detail="Course not found")
    result=get_student_course_by_id(current_user.id,course_id)
    if result=="Not found":
       raise HTTPException(status_code=403,detail="You have never been enrolled in this course")
    return result
    
