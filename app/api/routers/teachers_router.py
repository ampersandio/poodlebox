import api.utils.constants as constants

from fastapi import APIRouter,HTTPException,Depends, File, UploadFile,Form
from mariadb import IntegrityError
from fastapi.responses import JSONResponse
from api.data.models import User, CourseCreate, SectionCreate, ContentCreate, TeachersReport, TeacherProfile, EditTeacherProfile
from api.services.authorization import get_current_user, validate_password
from api.services import courses, report, users
from api.utils.utils import file_upload, mail_teachers_report
from typing import Annotated, Optional


teachers_router = APIRouter(prefix="/teachers", tags=["Teachers"])


@teachers_router.get("/courses/reports")
def get_report(current_user: Annotated[User, Depends(get_current_user)], send_email: bool = False) -> TeachersReport:
    '''
    Get Teachers Report
    '''

    if current_user.role.lower() != constants.TEACHER_ROLE:
        raise HTTPException(status_code=400, detail="Reports are currently only available for teachers")

    teachers_report = report.get_teachers_report(current_user)
    if teachers_report is None:
        raise HTTPException(status_code=200, detail="You either currently own no courses, or there are no students enrolled in any of your courses")
    
    if send_email:
        mail_teachers_report(teachers_report)

    return teachers_report


@teachers_router.get('/profiles/')
def view_profile(user: User = Depends(get_current_user)) -> TeacherProfile:
    '''
    View profile
    '''
    profile = TeacherProfile.from_user(user)
    return profile


@teachers_router.put('/profiles/')
def edit_profile(new_information: EditTeacherProfile, user: User = Depends(get_current_user)) -> JSONResponse:
    '''
    Edit profile
    '''
    if new_information.new_password != new_information.new_password_again:
        raise HTTPException(status_code=409, detail='Password does not match')
    
    validate_password(new_information.new_password)

    users.edit_teacher_profile(new_information, user)

    return JSONResponse(status_code=200, content={'msg': 'Profile updated'})


@teachers_router.post("/courses/")
def course_create(title: str = Form(...), description: str = Form(...), objectives: str = Form(...), premium: bool = Form(...), tags: list[str] = Form(...), file: UploadFile = File(None), current_user: User = Depends(get_current_user)):
    '''
    Create course with thumbnail attached as a file: Upload = File(...)
    '''

    if file:
        course = CourseCreate( title=title, description=description,  objectives=objectives, premium=premium, tags=tags, course_picture=file.filename)
        file_upload(file, "course_thumbnails", course)
    else:
        course = CourseCreate( title=title, description=description,  objectives=objectives, premium=premium, tags=tags)


    if current_user.role != constants.TEACHER_ROLE:
        raise HTTPException(status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL)
    
    if current_user.verified_email == False:
        raise HTTPException(status_code=403, detail="Your email is not verified")
    
    try:
        new_course = courses.create_course(course, current_user.id)

    except IntegrityError:
        raise HTTPException(status_code=409, detail="A course with that title already exists")
    
    if new_course != None:
        raise HTTPException(status_code=400, detail=new_course)

    return JSONResponse(status_code=201, content={"msg": "Course created"})


# # @teachers_router.post("/courses")
# def create_course(course: CourseCreate, current_user: User = Depends(get_current_user)):
#     '''
#     Create course functionality without a thumbnail
#     '''


#     return JSONResponse(status_code=201, content={"msg": "Course created"})


@teachers_router.post("/courses/{course_id}/thumbnail")
def upload_photo(course_id=int, file: UploadFile = File(...)):
    '''
    Add thumbnail to a course
    '''

    course = courses.get_course_by_id(course_id)

    if course is None:
        raise HTTPException(status_code=403, detail=constants.COURSE_NOT_FOUND_DETAIL)

    file_upload(file, "course_thumbnails", course)

    return {"message": f"Successfully uploaded {file.filename}"}


@teachers_router.post("/courses/{course_id}/sections/")
def add_section(section: SectionCreate, course_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    '''
    Add section to course
    '''

    course = courses.get_course_by_id(course_id)

    if course is None:
        raise HTTPException(status_code=404, detail=constants.COURSE_NOT_FOUND_DETAIL)

    if current_user.role != constants.TEACHER_ROLE or course.teacher.email != current_user.email:
        raise HTTPException(
            status_code=403,
            detail="This user does not have permission to add sections to this course")
    else:
        courses.create_section(course_id, section)

    return JSONResponse(status_code=201, content={"msg": "Section created"})


@teachers_router.put("/courses/{course_id}/sections/{section_id}")
def edit_section(course_id: int,section_id: int,new_section: SectionCreate,current_user: Annotated[User, Depends(get_current_user)]):
    '''
    Edit section
    '''

    course = courses.get_course_by_id(course_id)
    section = courses.get_section_by_id(section_id)
    sections = courses.get_course_sections(course_id)

    if new_section.title == section.title:
        raise HTTPException(
            status_code=403, detail="This Section already has the same name."
        )

    if course.teacher.email != current_user.email:
        raise HTTPException(status_code=403,detail=constants.SECTION_ACCESS_DENIED_DETAIL)

    if section is None:
        raise HTTPException(status_code=404, detail=constants.SECTION_NOT_FOUND_DETAIL)

    if course is None:
        raise HTTPException(status_code=404, detail=constants.COURSE_NOT_FOUND_DETAIL)

    if section.id not in [section.id for section in sections]:
        raise HTTPException(status_code=403, detail="This section is not part of this course")

    if new_section.content:
        for content in new_section.content:
            if content not in section.content:
                courses.add_content(section_id, content)
            else:
                raise HTTPException(status_code=403, detail="Content with this title already exist")

    courses.update_section(section_id, new_section)


@teachers_router.delete("/courses/{course_id}/sections/{section_id}")
def delete_section(course_id: int,section_id: int,current_user: Annotated[User, Depends(get_current_user)]):
    '''
    Delete section from a course
    '''

    course = courses.get_course_by_id(course_id)
    section = courses.get_section_by_id(section_id)
    sections = courses.get_course_sections(course_id)

    if course.teacher.email != current_user.email:
        raise HTTPException(status_code=403, detail=constants.SECTION_ACCESS_DENIED_DETAIL)

    if section is None:
        raise HTTPException(status_code=404, detail=constants.SECTION_NOT_FOUND_DETAIL)

    if course is None:
        raise HTTPException(status_code=404, detail=constants.COURSE_NOT_FOUND_DETAIL)

    if section.id not in [section.id for section in sections]:
        raise HTTPException(status_code=403, detail="This section is not part of this course")


    courses.delete_section(section_id)
    return JSONResponse(status_code=204, content={"msg": "Section Deleted Successfully"})


@teachers_router.post("/courses/{course_id}/sections/{section_id}/content")
async def add_content_to_section(course_id:int, section_id:int, title:str = Form(...), description:str = Form(...), content_type:str = Form(...), file: Optional[UploadFile] = File(None), current_user: User = Depends(get_current_user)):

    course = courses.get_course_by_id(course_id)
    section = courses.get_section_by_id(section_id)

    if current_user.role != constants.TEACHER_ROLE or course.teacher.email != current_user.email:
        raise HTTPException(status_code=403, detail="This user does not have permission to add sections to this course")

    elif not section:
        raise HTTPException(status_code=404, detail=constants.SECTION_NOT_FOUND_DETAIL)

    else:
        if file:
            link = file_upload(file,"documents",title)
            content = ContentCreate(title=title, description=description, content_type=content_type, link=link)
        else:
            content = ContentCreate(title=title, description=description, content_type=content_type)

    courses.add_content(section_id, content)
    return JSONResponse(status_code=201, content={"msg": "Content created"})


# Delete Content