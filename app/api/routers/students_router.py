from fastapi import APIRouter, Depends, HTTPException, Response, Header, Request
from typing import Annotated, Optional
from api.services.students import (
    enroll_in_course,
    get_students_number_courses_premium,
    check_enrollment_status,
)
from api.services.certificates import get_certificates, get_certificate_by_course
from api.data.models import User, Subscription, StudentEdit, CoursesShowStudent
from api.services.authorization import get_current_user
from api.services.courses import get_students_courses, get_student_course_by_id, get_course_by_id
from api.services.students import get_students_courses_id
from api.services.students import get_profile, change_password
from api.services.authorization import hash_password
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, paginate
from api.data import database
import api.utils.constants as constants
from api.utils.utils import enrollment_mail


students_router = APIRouter(prefix="/students", tags=["Students"])


@students_router.get("/courses/certificates")
def get_certificates_of_student(current_user: User = Depends(get_current_user)):
    """Get all the certificates of the student"""
    return get_certificates(current_user.id)


@students_router.get("courses/{course_id}/certificates")
def get_certificate_of_student_for_course(
    course_id: int, current_user: User = Depends(get_current_user)
):
    """Get the certificate of a particular course"""
    if course_id not in get_students_courses_id(current_user.id):
        raise HTTPException(
            status_code=403, detail=constants.NO_ENROLLMENT_FOUND
        )
    result = get_certificate_by_course(current_user.id, course_id)
    if result == None:
        raise HTTPException(
            status_code=404, detail=constants.CERTIFICATE_NOT_FOUND_DETAIL
        )
    return result


@students_router.get("/courses", response_model=Page[CoursesShowStudent])
def get_courses_for_student(
    current_user: User = Depends(get_current_user),
    sort=None,
    sort_by=None,
    title=None,
    subscription=None,
):
    """Get all the courses that the student has been enrolled in"""
    result = get_students_courses(current_user.id)
    if title:
        result = [x for x in result if title.lower() in x.title.lower()]
    if subscription:
        result = [x for x in result if subscription.lower() in x.subscription_status.lower()]
    if sort and (sort == "asc" or sort == "desc"):
        if sort_by == "id":
            result = sorted(result, key=lambda r: r.id, reverse=sort == "desc")
        elif sort_by == "rating":
            result = sorted(result, key=lambda r: r.rating, reverse=sort == "desc")
        elif sort_by == "progress":
            result = sorted(result, key=lambda r: r.progress, reverse=sort == "desc")
    return paginate(result)


@students_router.get("/profiles")
def get_student_profile(current_user: User = Depends(get_current_user)):
    """Get the profile of the student"""
    if current_user.role!='student':
        raise HTTPException(status_code=403,detail=constants.SECTION_ACCESS_DENIED_DETAIL)
    return get_profile(current_user.id)


@students_router.put("/profiles")
def change_student_profile(
    edited_info: StudentEdit, current_user: User = Depends(get_current_user)
):
    """Change the password of the sudent's profile"""
    if current_user.role!='student':
        raise HTTPException(status_code=403,detail=constants.SECTION_ACCESS_DENIED_DETAIL)
    if edited_info.new_password != edited_info.confirm_new_password:
        raise HTTPException(
            status_code=400, detail=constants.PASSWORD_DONT_MATCH
        )
    hashed_pass = hash_password(edited_info.confirm_new_password)
    change_password(current_user.id, hashed_pass)
    return JSONResponse(
        status_code=200, content={"msg" : constants.PASSWORD_CHANGED_SUCCESSFULLY }
    )


@students_router.get("/courses/{course_id}")
def get_course_for_student_by_id(
    course_id: int, current_user: User = Depends(get_current_user)
):
    """Get a course that the student has been enrolled in by id"""
    if get_course_by_id(course_id) == None:
        raise HTTPException(status_code=404, detail=constants.COURSE_NOT_FOUND_DETAIL)
    if course_id not in get_students_courses_id(current_user.id):
        raise HTTPException(
            status_code=403, detail=constants.NO_ENROLLMENT_FOUND
        )
    result = get_student_course_by_id(current_user.id, course_id)
    return result

@students_router.put("/courses/{course_id}")
def enroll_or_unenroll_from_course(
    course_id: int,
    subscription: Subscription,
    current_user: User = Depends(get_current_user),
):
    """Enroll or unenroll a student from a particular course"""

    course = get_course_by_id(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail=constants.COURSE_NOT_FOUND_DETAIL)

    result = check_enrollment_status(current_user.id, course_id)
    number = get_students_number_courses_premium(current_user.id)

    if result == None or result == 3:
        if subscription.enroll == False:
            raise HTTPException(status_code=400, detail=constants.NOTHING_TO_UPDATE)
        elif subscription.enroll == True and number < 5:
            enroll_in_course(current_user.id, course_id, subscription, result is not None)
            student = get_profile(current_user.id)
            teacher = course.teacher
            enrollment_mail(student, course, teacher)
            return JSONResponse(
                status_code=201, content={"msg": constants.REVIEW_REQUEST}
            )
        elif subscription.enroll == True and number == 5 and course.premium == False:
            enroll_in_course(current_user.id, course_id, subscription, result is not None)
            student = get_profile(current_user.id)
            teacher = course.teacher
            enrollment_mail(student, course, teacher)
            return JSONResponse(
                status_code=201, content={"msg": constants.REVIEW_REQUEST}
            )
        elif subscription.enroll == True and number == 5 and course.premium == True:
            raise HTTPException(status_code=400, detail=constants.NO_MORE_PREMIUM)

    elif result in [1, 2]:
        if subscription.enroll == True:
            raise HTTPException(status_code=400, detail=constants.NOTHING_TO_UPDATE)
        else:
            enroll_in_course(current_user.id, course_id, subscription, False)
            return JSONResponse(
                status_code=200,
                content={"msg": constants.SUCCESSFULL_UNENROLLMENT},
            )

    enroll_in_course(current_user.id, course_id, subscription, False)
    student = get_profile(current_user.id)
    teacher = course.teacher
    enrollment_mail(student, course, teacher)
    return JSONResponse(
        status_code=201, content={"msg": constants.REVIEW_REQUEST}
    )