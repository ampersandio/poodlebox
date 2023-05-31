from fastapi import APIRouter, Depends, HTTPException, Response, Header, Request
from fastapi.responses import JSONResponse
from typing import Annotated, Optional
from api.services import courses
from api.data.models import User, CourseCreate, SectionCreate, ContentCreate
from api.services.authorization import get_current_user, get_oauth2_scheme
from api.services.students import get_students_courses_id
from api.utils.utils import email_certificate

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
    
    print(courses.n_visited_sections(current_user.id,course.id))
    print(courses.n_sections_by_course_id(course.id)[0][2])

    if current_user.role == "student" and courses.n_visited_sections(
        current_user.id, course.id
    )[0][0] == courses.n_sections_by_course_id(course.id)[0][2]:
        courses.change_subscription(3, current_user.id, course.id)
        email_certificate(current_user,course.title)

    return section
