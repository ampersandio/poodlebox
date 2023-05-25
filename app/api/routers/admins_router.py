from fastapi import APIRouter, Depends, HTTPException, Response, Header, Request, File, UploadFile
from fastapi.responses import JSONResponse
from typing import Annotated, Optional
from api.services import courses

from api.services.authorization import get_current_user, get_oauth2_scheme
from api.services.students import get_profile
from api.services.courses import get_course_by_id, get_courses_students
from api.services.admins import student_status, course_status, pending_registrations, approve_registration
from api.services.users import get_user_by_id
from api.utils.utils import teacher_approval, course_deactivated

admins_router = APIRouter(prefix="/admins", tags=["Admins"])


@admins_router.put("/students/{student_id}/status/{disabled}")
def change_student_status(student_id: int, disabled: bool, current_user = Depends(get_current_user)):
    '''
    Change Student Status
    '''

    student = get_profile(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student with this Id does not exist")

    if current_user.role == "admin":
        student_status(student_id, disabled)
    else:
        raise HTTPException(status_code=403, detail="You're not allowed in the admin section")
    
    return JSONResponse(status_code=201, content="Students status updated")


@admins_router.put("/courses/{course_id}/status/{disabled}")
def change_course_status(course_id: int, disabled: bool, current_user = Depends(get_current_user)):
    '''
    Change Course Status
    '''

    course = get_course_by_id(course_id)

    if course is None:
        raise HTTPException(status_code=404, detail="Course with this Id does not exist")

    students = get_courses_students(course_id)

    if current_user.role == "admin":
        course_status(course_id, disabled)

        for student in students:
            course_deactivated(student, course.title)

    else:
        raise HTTPException(status_code=403, detail="You're not allowed in the admin section")
    
    return JSONResponse(status_code=201, content="Course status updated")


@admins_router.put("/courses/{course_id}/students/{student_id}")
def remove_student_from_course(course_id: int, student_id: int, current_user = Depends(get_current_user)):
    '''
    Remove Student From a Course
    '''

    course = get_course_by_id(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course with this Id does not exist")
    
    student = get_profile(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student with this Id does not exist")

    if current_user.role == "admin":
        remove_student_from_course(course_id,student_id)
    else:
        raise HTTPException(status_code=403, detail="You're not allowed in the admin section")
    
    return JSONResponse(status_code=201, content="Student removed")


@admins_router.get("/registrations/")
def get_pending(current_user = Depends(get_current_user)):
    '''
    Get Current Pending Registrations
    '''

    if current_user.role == "admin":
        return pending_registrations()
    else:
        raise HTTPException(status_code=403, detail="You're not allowed in the admin section")


@admins_router.put("/registrations/{teacher_id}")
def approve(teacher_id: int, current_user = Depends(get_current_user)):
    '''
    Approve Teachers Registration
    '''

    teacher = get_user_by_id(teacher_id)

    teacher_approval(teacher)

    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher with this Id does not exist")

    if current_user.role == "admin":
        approve_registration(teacher_id)

    else:
        raise HTTPException(status_code=403, detail="You're not allowed in the admin section")

    return JSONResponse(status_code=201, content="Teacher registration approved")

# Probably would go in the courses section as and would check for admin privileges 
# @admins_router.get("/courses")
# def search_courses(teacher_id: int = None, student_id: int = None):
#     # Implementation for searching courses, optionally filtered by teacher_id and/or student_id
#     pass

@admins_router.get("/ratings/traceback")
def traceback_ratings():
    # Implementation for retrieving ratings traceback
    pass