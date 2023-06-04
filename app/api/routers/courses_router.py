import api.utils.constants as constants

from fastapi import APIRouter, Depends, HTTPException, Request

from typing import Annotated
from api.services import courses
from api.data.models import User, Section, CourseShow
from fastapi_pagination import Page, paginate
from api.services.authorization import get_current_user, get_oauth2_scheme
from api.services.students import get_students_courses_id, check_enrollment_status
from api.utils.utils import email_certificate
from fastapi_pagination import Page,paginate

courses_router = APIRouter(prefix="/courses", tags=["Courses"])

custom_oauth2_scheme = get_oauth2_scheme(auto_error=False)


@courses_router.get("/",response_model=Page[CourseShow])
def get_all_courses(
    current_user: User | None = Depends(custom_oauth2_scheme),
    title=None,
    tag=None,
    sort=None,
    sort_by=None,
):
    """Get all the courses that the current user has access to"""
    if current_user:
        user = get_current_user(current_user)
        if user.role == constants.TEACHER_ROLE:
            result = courses.get_courses_teacher()
        elif user.role == constants.STUDENT_ROLE:
            result = courses.get_courses_student(user.id)
        else:
            result = courses.get_courses_teacher()
    else:
        result = courses.get_courses_anonymous()

    if title:
        result = [x for x in result if title.lower() in x.title.lower()]
    if tag:
        result = [x for x in result if tag in x.tags]

    if sort and (sort == "asc" or sort == "desc"):
        if sort_by == "id":
            result = sorted(result, key=lambda r: r.id, reverse=sort == "desc")
        elif sort_by == "rating":
            result = sorted(result, key=lambda r: r.rating, reverse=sort == "desc")

    return paginate(result)

# should fix this 
@courses_router.get("/popular")
def get_most_popular_courses(request: Request):
    """Get the most popular courses"""
    return courses.get_most_popular()


@courses_router.get("/{course_id}")
def get_course_by_id(
    course_id: int, current_user: Annotated[User, Depends(get_current_user)]
):
    """Get a course by its id"""
    result = courses.get_course_by_id(course_id)
    if result is None:
        raise HTTPException(status_code=404, detail=constants.COURSE_NOT_FOUND_DETAIL)
    if (
        current_user.role == constants.STUDENT_ROLE
        and result.id not in get_students_courses_id(current_user.id)
        and result.premium is True
    ):
        raise HTTPException(status_code=402, detail=constants.COURSE_ACCESS_DENIED_DETAIL)
    return result


@courses_router.get("/{course_id}/sections/", response_model=Page[Section])
def get_course_sections(course_id: int, current_user: User = Depends(get_current_user), search: str = None, sort_by: str = None) -> Page[Section]:
    """Get all the sections of a particular course with pagination and sorting"""

    course = courses.get_course_by_id(course_id)

    if (current_user.role not in [constants.TEACHER_ROLE, constants.STUDENT_ROLE]) and (course.id not in get_students_courses_id(current_user.id)):
        raise HTTPException(status_code=401, detail=constants.SECTION_ACCESS_DENIED_DETAIL)

    sections = course.sections

    if search:
        sections = [section for section in sections if search.lower() in section.title.lower()]

    return paginate(sorted(sections, key=lambda s: s.id, reverse = sort_by == "desc"))


@courses_router.get("/{course_id}/sections/{section_id}")
def get_section_by_id(course_id: int,section_id: int,current_user: Annotated[User, Depends(get_current_user)]):
    """Get a specific section from a course by its id"""

    course = courses.get_course_by_id(course_id)
    student_courses = get_students_courses_id(current_user.id)
    section = courses.get_section_by_id(section_id)

    if current_user.role not in [constants.TEACHER_ROLE, constants.STUDENT_ROLE] and course.id not in student_courses:
        raise HTTPException(status_code=401, detail=constants.SECTION_ACCESS_DENIED_DETAIL)

    if course is None:
        raise HTTPException(status_code=404, detail=constants.COURSE_NOT_FOUND_DETAIL)

    if section is None:
        raise HTTPException(status_code=404, detail=constants.SECTION_NOT_FOUND_DETAIL)

    if current_user.role == constants.STUDENT_ROLE:
        courses.visit_section(current_user.id, section.id)
    
    if current_user.role == constants.STUDENT_ROLE and courses.n_visited_sections(current_user.id, course.id) == courses.n_sections_by_course_id(course.id):
        if check_enrollment_status(current_user.id,course_id) == "1" and courses.change_subscription(constants.SUBSCRIPTION_EXPIRED, current_user.id, course.id) is not None:
            email_certificate(current_user,course.title)
            
    return section
