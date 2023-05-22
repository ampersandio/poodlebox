from fastapi import APIRouter, Depends, HTTPException, Response, Header, Request
from fastapi.responses import JSONResponse
from typing import Annotated, Optional
from api.services import courses
from api.data.models import User, CourseCreate, SectionCreate, ContentCreate
from api.services.authorization import get_current_user, get_oauth2_scheme
from api.services.students import get_students_courses_id

courses_router = APIRouter(prefix="/courses", tags=["Courses"])

custom_oauth2_scheme = get_oauth2_scheme(auto_error=False)

@courses_router.get("/")
def get_all_courses(current_user: User | None = Depends(custom_oauth2_scheme)):
    if current_user:
        user = get_current_user(current_user)

        return {"message": "You are logged in."}
    else:
        return {"message": "You are not logged in."}

#     request: Request,
#     token: str = Header({"detail":"Unauthorized"}None),
#     title=None,
#     tag=None,
#     sort=None,
#     sort_by=None,
# ):
#     if "authorization" not in request.headers.keys() and token is None:
#         result = courses.get_courses_anonymous()
#     elif token is not None and get_current_user(token).role == "student":
#         result = courses.get_courses_student(get_current_user(token).id)
#     elif token is not None and get_current_user(token).role == "teacher":
#         result = courses.get_courses_teacher()
#     elif (
#         "authorization" in request.headers.keys() and get_current_user(request.headers.get("authorization")[7:]).role == "student"
#     ):
#         result = courses.get_courses_student(
#             get_current_user(request.headers.get("authorization")[7:]).id
#         )
#     elif (
#         "authorization" in request.headers.keys() and get_current_user(request.headers.get("authorization")[7:]).role == "teacher"
#     ):
#         result = courses.get_courses_teacher()
#     else:
#         raise HTTPException(status_code=401, detail="User not authenticated")
#     if title:
#         result = [x for x in result if title.lower() in x.title.lower()]
#     if tag:
#         result = [x for x in result if tag in x.tags]

#     if sort and (sort == "asc" or sort == "desc"):
#         if sort_by == "id":
#             result = sorted(result, key=lambda r: r.id, reverse=sort == "desc")
#         elif sort_by == "rating":
#             result = sorted(result, key=lambda r: r.rating, reverse=sort == "desc")

#     return result


@courses_router.get("/popular")
def get_most_popular_courses(request: Request):
    if "authorization" in request.headers.keys():
        token = request.headers.get("authorization")[7:]
        user_role = get_current_user(token).role
        return courses.get_most_popular(user_role)
    else:
        return courses.get_most_popular(None)
    

@courses_router.get("/{course_id}")
def get_course_by_id(
    course_id, current_user: Annotated[User, Depends(get_current_user)]
):
    result = courses.get_course_by_id(course_id)
    if result == "Not found":
        raise HTTPException(status_code=404, detail="Course not found")
    if (
        current_user.role == "Student"
        and result.id not in get_students_courses_id(current_user.id)
        and result.premium is True
    ):
        raise HTTPException(
            status_code=402, detail="You don't have access to this course"
        )
    return result


@courses_router.post("/")
def create_course(course: CourseCreate, current_user: User = Depends(get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403, detail="You don't have access to this section"
        )
    course_result=courses.get_course_by_title(course.title)
    if course_result!="Not found":
        raise HTTPException(
            status_code=400, detail="A course with that title already exists"
        )     
    if current_user.verified_email == False:
        raise HTTPException(status_code=403, detail="Your email is not verified")
    new_course=courses.create_course(course, current_user.id)
    if new_course!=None:
        raise HTTPException(
            status_code=400, detail=new_course
        )   
    return JSONResponse(status_code=201, content={"msg":"Course created"})


@courses_router.get("/{course_id}/sections/")
def get_course_sections(course_id, current_user: Annotated[User, Depends(get_current_user)]):  
    course = courses.get_course_by_id(course_id)

    if (current_user.role not in ["teacher", "admin"]) and(course.id not in get_students_courses_id(current_user.id)):
        raise HTTPException(status_code=401,detail="You don't have access to this section")
    else:
        return course.sections
    

@courses_router.get("/{course_id}/sections/{section_id}")
def get_section_by_id(course_id:int, section_id:int, current_user: Annotated[User, Depends(get_current_user)]):
    course = courses.get_course_by_id(course_id)
    student_courses = get_students_courses_id(current_user.id)
    
    if current_user.role not in ["teacher", "admin"] and course.id not in student_courses:
        raise HTTPException(status_code=401, detail="You don't have access to this section")
    
    if course is None:
        raise HTTPException(status_code=404, detail="Course with this ID does not exist")
    
    section = courses.get_section_by_id(section_id)
    
    if section is None:
        raise HTTPException(status_code=404, detail="Section with this ID does not exist")
    
    if current_user.role == "student":
        courses.visited_section(current_user.id, section.id)
    
    if (current_user.role == "student" and courses.n_visited_sections(current_user.id, course.id) == courses.n_sections_by_course_id(course.id)):
        courses.change_subscription(3, current_user.id, course.id)
    
    return section


@courses_router.post("/{course_id}/sections/")
def add_section(section: SectionCreate, course_id:int, current_user: Annotated[User, Depends(get_current_user)]):
    course = get_course_by_id(course_id, current_user)
    if current_user.role != "teacher" or course.teacher.email != current_user.email:
        raise HTTPException(status_code=403, detail="This user does not have permission to add sections to this course")
    else:
        courses.create_section(course_id,section)

    return JSONResponse(status_code=201, content={"msg":"Section created"})


@courses_router.post("/{course_id}/sections/{section_id}/content")
def add_content_to_section(course_id:int, section_id:int, content:ContentCreate, current_user: Annotated[User, Depends(get_current_user)]):
    course = get_course_by_id(course_id, current_user)
    section = get_section_by_id(course_id,section_id,current_user)

    if current_user.role != "teacher" or course.teacher.email != current_user.email:
        raise HTTPException(status_code=403, detail="This user does not have permission to add sections to this course")
    
    elif not section:
        raise HTTPException(status_code=404, detail="Section with this Id does not exist")

    else:
        courses.add_content(section_id,content)
        return JSONResponse(status_code=201, content={"msg":"Content created"})

