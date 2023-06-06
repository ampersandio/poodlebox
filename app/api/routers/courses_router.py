import api.utils.constants as constants

from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import JSONResponse

from typing import Annotated, Optional
from api.services import courses
from api.data.models import User, Section, CourseShow
from fastapi_pagination import Page, paginate
from api.data.models import User, CourseCreate, SectionCreate, ContentCreate, PendingEnrollment
from api.services.authorization import get_current_user, get_oauth2_scheme
from api.services.students import get_students_courses_id, check_enrollment_status, update_interest, check_enrollment_status
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
def get_section_by_id(course_id:int ,section_id:int ,current_user:Annotated[User, Depends(get_current_user)]):
    """Get a specific section from a course by its id"""

    course = courses.get_course_by_id(course_id)
    student_courses = get_students_courses_id(current_user.id)
    section = courses.get_section_by_id(section_id)


    if current_user.role not in [constants.TEACHER_ROLE, constants.STUDENT_ROLE]:
        raise HTTPException(status_code=401, detail=constants.SECTION_ACCESS_DENIED_DETAIL)
    
    if current_user.role == constants.STUDENT_ROLE and course.id not in student_courses:
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


@courses_router.post('/{course_id}/reviews')
def post_review(course_id: int,  user: User = Depends(get_current_user), rating: float = Form(...), description: Optional[str] = Form(None)) -> JSONResponse:
    if (enrollment := check_enrollment_status(user.id, course_id)) in ['No status', 2]:
        raise HTTPException(status_code=409, detail=f'You must be currently or previously enrolled in course: {course_id} to leave a review, your current enrollment status is: {enrollment}')
    
    left_review = courses.leave_review(user.id, course_id, rating, description)
    if left_review == False:
        raise HTTPException(status_code=409, detail=f'User: {user.id} has already left a review for course: {course_id}')
    
    return JSONResponse(status_code=201, content={'msg': 'review created'})


@courses_router.put('/{course_id}/status')
def change_course_status(course_id: int, active: bool = Form(...), user: User = Depends(get_current_user)) -> JSONResponse:
    
    if active == True:
        if user.role.lower() != 'admin':
            owner_id = courses.get_course_owner(course_id)
            if owner_id != user.id:
                raise HTTPException(status_code=401, detail=f'Only the owner of a course can change its status, you are user: {user.id}, owner for course: {course_id} is: {owner_id}')
        
        activated = courses.activate_course(course_id)        
        if activated == False:
            raise HTTPException(status_code=409, detail=f'Course: {course_id} either not found, or already active')
        
        return JSONResponse(status_code=200, content={'msg': f'Course: {course_id} activated'})
    
    if active == False:
        if user.role.lower() != 'admin':
            owner_id = courses.get_course_owner(course_id)
            if owner_id != user.id:
                raise HTTPException(status_code=401, detail=f'Only the owner of a course can change its status, you are user: {user.id}, owner for course: {course_id} is: {owner_id}')
        
        deactivated = courses.deactivate_course(course_id)        
        if deactivated == False:
            raise HTTPException(status_code=409, detail=f'Course: {course_id} either not found, or already not active')
        
        return JSONResponse(status_code=200, content={'msg': f'Course: {course_id} deactivated'})
    

@courses_router.get('/pending_enrollments/reports')
def get_pending_enrollments(user: User = Depends(get_current_user)) -> list[PendingEnrollment]:
    pending_enrollments = courses.get_pending_enrollments(user.id)
    if pending_enrollments is None:
        raise HTTPException(status_code=404, detail=f'No pending enrollments for courses with owner: {user.id}')
    
    return pending_enrollments


@courses_router.put('/pending_enrollments')
def judge_enrollment(user_id: int = Form(...), course_id: int = Form(...), approved: bool = Form(...), user: User = Depends(get_current_user)) -> JSONResponse:
    if user.role.lower() != 'admin':
        owner = courses.get_course_owner(course_id)
        if owner != user.id:
            raise HTTPException(status_code=401, detail=f'Only the owner of course: {course_id} can judge enrollments for it')

    if approved:
        enrolled = courses.approve_enrollment(user_id, course_id)
        if not enrolled:
            raise HTTPException(status_code=404, detail=f'No enrollment request found for user: {user_id} in course: {course_id}')
        
        update_interest(user_id, course_id)
        return JSONResponse(status_code=200, content={'msg': f'Enrollment for user: {user_id} in course: {course_id} approved'})
    
    if not approved:
        rejected = courses.reject_enrollment(user_id, course_id)
        if not rejected:
            raise HTTPException(status_code=404, detail=f'No enrollment request found for user: {user_id} in course: {course_id}')
        
        update_interest(user_id, course_id)
        return JSONResponse(status_code=200, content={'msg': f'Enrollment for user: {user_id} in course: {course_id} rejected'})