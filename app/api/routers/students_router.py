from fastapi import APIRouter, Depends, HTTPException, Response, Header, Request
from typing import Annotated, Optional
from api.services.students import enroll_in_course,get_students_number_courses_premium,check_enrollment_status
from api.services.certificates import get_certificates,get_certificate_by_course
from api.data.models import User, Subscription, StudentEdit
from api.services.authorization import get_current_user
from api.services.courses import (
    get_students_courses,
    get_student_course_by_id,
    get_course_by_id,
)
from api.services.students import get_students_courses_id
from api.services.students import get_profile, change_password
from api.services.authorization import hash_password
from fastapi.responses import JSONResponse


students_router = APIRouter(prefix="/students", tags=["Students"])

@students_router.get("/courses/certificates")
def get_certificates_of_student(current_user: User = Depends(get_current_user)):
    return get_certificates(current_user.id)

@students_router.get("courses/{course_id}/certificates")
def get_certificate_of_student_for_course(course_id:int,current_user: User = Depends(get_current_user)):
    if course_id not in get_students_courses_id(current_user.id):
        raise HTTPException(status_code=403,detail="You have never been enrolled in this course")
    result=get_certificate_by_course(current_user.id,course_id)
    if result==None:
        raise HTTPException(status_code=404,detail="Certificate for this course not found")
    return result


@students_router.get("/courses")
def get_courses_for_student(
    current_user: User = Depends(get_current_user),
    sort=None,
    sort_by=None,
    title=None,
    subscription=None,
):
    result = get_students_courses(current_user.id)
    if title:
        result = [x for x in result if title.lower() in x.title.lower()]
    if subscription:
        result = [x for x in result if subscription.lower() in x.subscription.lower()]
    if sort and (sort == "asc" or sort == "desc"):
        if sort_by == "id":
            result = sorted(result, key=lambda r: r.id, reverse=sort == "desc")
        elif sort_by == "rating":
            result = sorted(result, key=lambda r: r.rating, reverse=sort == "desc")
        elif sort_by == "progress":
            result = sorted(result, key=lambda r: r.progress, reverse=sort == "desc")
    return result


@students_router.get("/profiles")
def get_student_profile(current_user: User = Depends(get_current_user)):
    return get_profile(current_user.id)


@students_router.put("/profiles")
def change_student_profile(
    edited_info: StudentEdit, current_user: User = Depends(get_current_user)
):
    if edited_info.new_password != edited_info.confirm_new_password:
        raise HTTPException(
            status_code=400, detail="New password and confirm password don't match"
        )
    hashed_pass = hash_password(edited_info.confirm_new_password)
    change_password(current_user.id, hashed_pass)
    return JSONResponse(
        status_code=200, content={"msg": "Password changed successfully"}
    )



@students_router.get("/courses/{course_id}")
def get_course_for_student_by_id(
    course_id:int, current_user: User = Depends(get_current_user)
):
    if get_course_by_id(course_id) == None:
        raise HTTPException(status_code=404, detail="Course not found")
    if course_id not in get_students_courses_id(current_user.id):
        raise HTTPException(
            status_code=403, detail="You have never been enrolled in this course"
        )
    result = get_student_course_by_id(current_user.id, course_id)
    return result


@students_router.put("/courses/{course_id}")
def enroll_or_unenroll_from_course(
    course_id:int,
    subscription: Subscription,
    current_user: User = Depends(get_current_user),
):  
    course=get_course_by_id(course_id)
    if course == None:
        raise HTTPException(status_code=404, detail="Course not found")
    result = check_enrollment_status(current_user.id, course_id)
    number= get_students_number_courses_premium(current_user.id)
    if (result == "No status" or result==3) and subscription.enroll==False:
        raise HTTPException(status_code=400, detail="There is nothing to update")
    elif (result == "No status" or result==3) and subscription.enroll==True and number<5:
        if result=="No status":
         enroll_in_course(current_user.id,course_id,subscription,False)
        else:
         enroll_in_course(current_user.id,course_id,subscription,True) 
        return JSONResponse(
            status_code=201, content={"msg": "Your request has been sent for review"}
        )
    elif (result == "No status" or result==3) and subscription.enroll==True and number==5 and course.premium==False:
        if result=="No status":
         enroll_in_course(current_user.id,course_id,subscription,False)
        else:
         enroll_in_course(current_user.id,course_id,subscription,True) 
        return JSONResponse(
            status_code=201, content={"msg": "Your request has been sent for review"}
        )
    elif (result == "No status" or result==3)  and subscription.enroll==True and number==5 and course.premium==True:
        raise HTTPException(status_code=400,detail="You can't enroll in any more premium courses")
    elif result in [1,2] and subscription.enroll==True:
        raise HTTPException(status_code=400, detail="There is nothing to update")
    
    elif result in [1,2] and subscription.enroll==False:
        enroll_in_course(current_user.id,course_id,subscription, False)
        return JSONResponse(
        status_code=200,
        content={"msg": "You have successfully unenrolled from the course"},
    )
    enroll_in_course(current_user.id,course_id,subscription,False)
    return JSONResponse(status_code=201, content={"msg": "Your request has been sent for review"})



