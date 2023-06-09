import api.utils.constants as constants

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from api.services.authorization import get_current_user
from api.services.students import get_profile
from api.services.courses import get_course_by_id, get_course_students
from api.services.admins import student_status, course_status, pending_registrations, approve_registration
from api.services.users import get_user_by_id
from api.utils.utils import teacher_approval_mail, course_deactivated_mail

admins_router = APIRouter(prefix="/admins", tags=["Admins"])


@admins_router.put("/students/{student_id}/status/{disabled}")
def change_student_status(student_id: int, disabled: bool, current_user = Depends(get_current_user)):
    '''
    Change Student Status
    '''

    student = get_profile(student_id)

    if student is None:
        raise HTTPException(status_code=404, detail=constants.STUDENT_NOT_FOUND_DETAIL)

    if current_user.role == constants.ADMIN_ROLE:
        student_status(student_id, disabled)
    else:
        raise HTTPException(status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL)
    
    return JSONResponse(status_code=201, content=constants.STUDENT_UPDATED)


@admins_router.put("/courses/{course_id}/status/{disabled}")
def change_course_status(course_id: int, disabled: bool, current_user = Depends(get_current_user)):
    '''
    Change Course Status
    '''

    course = get_course_by_id(course_id)

    if course is None:
        raise HTTPException(status_code=404, detail=constants.COURSE_NOT_FOUND_DETAIL)

    students = get_course_students(course_id)

    if current_user.role == constants.ADMIN_ROLE:
        course_status(course_id, disabled)

        for student in students:
            course_deactivated_mail(student, course.title)

    else:
        raise HTTPException(status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL)
    
    return JSONResponse(status_code=201, content=constants.COURSE_UPDATED)


@admins_router.put("/courses/{course_id}/students/{student_id}")
def remove_student_from_course(course_id: int, student_id: int, current_user = Depends(get_current_user)):
    '''
    Remove Student From a Course
    '''

    course = get_course_by_id(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail=constants.COURSE_NOT_FOUND_DETAIL)
    
    student = get_profile(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail=constants.STUDENT_NOT_FOUND_DETAIL)

    if current_user.role == constants.ADMIN_ROLE:
        remove_student_from_course(course_id,student_id)
    else:
        raise HTTPException(status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL)
    
    return JSONResponse(status_code=201, content=constants.STUDENT_REMOVED)


@admins_router.get("/registrations/")
def get_pending(current_user = Depends(get_current_user)):
    '''
    Get Current Pending Registrations
    '''

    if current_user.role == constants.ADMIN_ROLE:
        return pending_registrations()
    else:
        raise HTTPException(status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL)


@admins_router.put("/registrations/{teacher_id}")
def approve(request:Request, teacher_id: int, current_user = Depends(get_current_user)):
    '''
    Approve Teachers Registration
    '''
    host = "http://" + request.headers["host"]

    teacher = get_user_by_id(teacher_id)

    teacher_approval_mail(teacher,host)

    if teacher is None:
        raise HTTPException(status_code=404, detail=constants.TEACHER_NOT_FOUND_DETAIL)

    if current_user.role == constants.ADMIN_ROLE:
        approve_registration(teacher_id)

    else:
        raise HTTPException(status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL)

    return JSONResponse(status_code=201, content=constants.TEACHER_APPROVED)

# Probably would go in the courses section as and would check for admin privileges 
# @admins_router.get("/courses")
# def search_courses(teacher_id: int = None, student_id: int = None):
#     # Implementation for searching courses, optionally filtered by teacher_id and/or student_id
#     pass

@admins_router.get("/ratings/traceback")
def traceback_ratings():
    # Implementation for retrieving ratings traceback
    pass