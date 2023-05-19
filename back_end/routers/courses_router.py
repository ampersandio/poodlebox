
from fastapi import APIRouter, Depends, HTTPException, Response
from services import courses_service

courses_router = APIRouter(prefix="/courses")


@courses_router.get("/")
def get_all_courses(current_user=None,title=None,tag=None,sort=None,sort_by=None):
    if current_user is None or current_user.role=="Teacher":
        result=courses_service.get_courses_anonymous_and_teacher()
    elif current_user.role=="Student":
        result=courses_service.get_course_by_id(current_user.id)
    
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
def get_course_by_id(course_id,current_user=None):
    result=courses_service.get_course_by_id(course_id)
    if result=='Not found':
        raise HTTPException(status_code=404,detail="Course not found")
    if current_user is not None and current_user.role=="Student" and result.id not in current_user.access:
        raise  HTTPException(status_code=402,detail="You don't have access to this course")
    
    return result




