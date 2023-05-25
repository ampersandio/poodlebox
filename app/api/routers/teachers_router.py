from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from api.data.models import User,CourseCreate, SectionCreate, ContentCreate, TeachersReport
from api.services.authorization import get_current_user
from api.services import courses,report
from typing import Annotated


teachers_router = APIRouter(prefix="/teachers", tags=["Teachers"])


@teachers_router.get('/courses/reports')
def get_report(current_user: Annotated[User, Depends(get_current_user)]) -> TeachersReport:
    if current_user.role.lower() != 'teacher':
        raise HTTPException(status_code=400, detail='Reports are currently only available for teachers')
    
    teachers_report = report.get_teachers_report(current_user)
    if teachers_report is None:
        raise HTTPException(status_code=204, detail='You either currently own no courses, or there are no students enrolled in any of your courses')

    return teachers_report

@teachers_router.post("/courses")
def create_course(course: CourseCreate, current_user: User = Depends(get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403, detail="You don't have access to this section"
        )
    course_result=courses.get_course_by_title(course.title)
    if course_result!=None:
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


@teachers_router.post("/{course_id}/sections/")
def add_section(section: SectionCreate, course_id:int, current_user: Annotated[User, Depends(get_current_user)]):
    course = courses.get_course_by_id(course_id, current_user)
    if current_user.role != "teacher" or course.teacher.email != current_user.email:
        raise HTTPException(status_code=403, detail="This user does not have permission to add sections to this course")
    else:
        courses.create_section(course_id,section)

    return JSONResponse(status_code=201, content={"msg":"Section created"})


@teachers_router.post("/{course_id}/sections/{section_id}/content")
def add_content_to_section(course_id:int, section_id:int, content:ContentCreate, current_user: Annotated[User, Depends(get_current_user)]):
    course = courses.get_course_by_id(course_id, current_user)
    section = courses.get_section_by_id(course_id,section_id,current_user)

    if current_user.role != "teacher" or course.teacher.email != current_user.email:
        raise HTTPException(status_code=403, detail="This user does not have permission to add sections to this course")
    
    elif not section:
        raise HTTPException(status_code=404, detail="Section with this Id does not exist")

    else:
        courses.add_content(section_id,content)
        return JSONResponse(status_code=201, content={"msg":"Content created"})