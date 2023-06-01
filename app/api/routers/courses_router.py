from fastapi import APIRouter, Depends, HTTPException, Response, Header, Request, Form
from fastapi.responses import JSONResponse
from typing import Annotated, Optional
from api.services import courses
from api.data.models import User, CourseCreate, SectionCreate, ContentCreate
from api.services.authorization import get_current_user, get_oauth2_scheme
from api.services.students import get_students_courses_id, check_enrollment_status

courses_router = APIRouter(prefix="/courses", tags=["Courses"])

custom_oauth2_scheme = get_oauth2_scheme(auto_error=False)

@courses_router.get("/")
def get_all_courses(
    current_user: User | None = Depends(custom_oauth2_scheme),
    title=None,
    tag=None,
    sort=None,
    sort_by=None,
):
    if current_user:
        user = get_current_user(current_user)
        if user.role == "teacher":
            result = courses.get_courses_teacher()
        elif user.role == "student":
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

    return result


@courses_router.get("/popular")
def get_most_popular_courses(request: Request):
    return courses.get_most_popular()


@courses_router.get("/{course_id}")
def get_course_by_id(
    course_id: int, current_user: Annotated[User, Depends(get_current_user)]
):
    result = courses.get_course_by_id(course_id)
    if result == None:
        raise HTTPException(status_code=404, detail="Course not found")
    if (
        current_user.role == "Student"
        and result.id not in get_students_courses_id(current_user.id)
        and result.premium is True
    ):
        raise HTTPException(status_code=402, detail="You don't have access to this course")
    return result


@courses_router.get("/{course_id}/sections/")
def get_course_sections(
    course_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    search: str | None = None,
):
    course = courses.get_course_by_id(course_id)

    if (current_user.role not in ["teacher", "admin"]) and (
        course.id not in get_students_courses_id(current_user.id)
    ):
        raise HTTPException(
            status_code=401, detail="You don't have access to this section"
        )
    else:
        return course.sections


@courses_router.get("/{course_id}/sections/{section_id}")
def get_section_by_id(
    course_id: int,
    section_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
):
    course = courses.get_course_by_id(course_id)
    student_courses = get_students_courses_id(current_user.id)

    if (
        current_user.role not in ["teacher", "admin"]
        and course.id not in student_courses
    ):
        raise HTTPException(
            status_code=401, detail="You don't have access to this section"
        )

    if course is None:
        raise HTTPException(
            status_code=404, detail="Course with this ID does not exist"
        )

    section = courses.get_section_by_id(section_id)

    if section is None:
        raise HTTPException(
            status_code=404, detail="Section with this ID does not exist"
        )

    if current_user.role == "student":
        courses.visited_section(current_user.id, section.id)

    if current_user.role == "student" and courses.n_visited_sections(
        current_user.id, course.id
    ) == courses.n_sections_by_course_id(course.id):
        courses.change_subscription(3, current_user.id, course.id)

    return section


@courses_router.post('/{course_id}/reviews')
def post_review(course_id: int,  user: User = Depends(get_current_user), rating: float = Form(...), description: Optional[str] = Form(None)) -> JSONResponse:
    if (enrollment := check_enrollment_status(user.id, course_id)) in ['No status', 2]:
        raise HTTPException(status_code=409, detail=f'You must be currently or previously enrolled in course: {course_id} to leave a review, your current enrollment status is: {enrollment}')
    
    left_review = courses.leave_review(user.id, course_id, rating, description)
    if left_review == False:
        raise HTTPException(status_code=409, detail=f'User: {user.id} has already left a review for course: {course_id}')
    
    return JSONResponse(status_code=201, content={'msg': 'review created'})