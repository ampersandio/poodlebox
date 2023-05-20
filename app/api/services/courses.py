from api.data.database import read_query, insert_query
from api.data.models import (
    TeacherShow,
    CourseShow,
    Section,
    Content,
    CourseShowId,
    CoursesShowStudent,
    CourseCreate,
)


def get_courses_anonymous():
    data = read_query(
        "select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0) as rating,c.price,group_concat(distinct t.name) as tags,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id where c.premium=0 group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile,c.premium,u.id"
    )
    list_courses = []
    for x in range(len(data)):
        owner = TeacherShow.read_from_query_result(*data[x][8:])
        course = CourseShow.read_from_query_result(*data[x][:8], teacher=owner)
        list_courses.append(course)
    return list_courses


def get_courses_teacher():
    data = read_query(
        "select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0) as rating,c.price,group_concat(distinct t.name) as tags,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile,c.premium,u.id"
    )
    list_courses = []
    for x in range(len(data)):
        owner = TeacherShow.read_from_query_result(*data[x][8:])
        course = CourseShow.read_from_query_result(*data[x][:8], teacher=owner)
        list_courses.append(course)
    return list_courses


def get_courses_student(student_id):
    data_courses = read_query(
        "select c.id from courses c join users_has_courses uc on uc.courses_id=c.id where uc.users_id=? and (uc.subscriptions_id=? or uc.subscriptions_id=?)",
        (student_id, 2, 3),
    )
    if data_courses == []:
        return get_courses_teacher()
    data = read_query(
        "select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0) as rating,c.price,group_concat(distinct t.name) as tags,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id where t.name in (select t.name from tags t join interests i on t.id=i.tags_id where i.users_id=?) and c.id not in (select c.id from courses c left join users_has_courses uc on c.id=uc.courses_id where uc.users_id=?) group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile,u.id,c.premium  union select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0) as rating,c.price,group_concat(distinct t.name) as tags,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id left join users_has_courses uc on uc.courses_id=c.id where t.name not in (select t.name from tags t join interests i on t.id=i.tags_id where i.users_id=?) and c.id not in (select c.id from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id where t.name in (select t.name from tags t join interests i on t.id=i.tags_id where i.users_id=?) and c.id not in (select c.id from courses c left join users_has_courses uc on c.id=uc.courses_id where uc.users_id=?) group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile,u.id,c.premium )  group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile,c.id,c.premium,u.id union select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0)  as rating,c.price,group_concat(distinct t.name) as tags,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id where c.id in (select c.id from courses c join users_has_courses uc on c.id=uc.courses_id where uc.users_id=?) group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile,u.id,c.premium",
        (student_id, student_id, student_id, student_id, student_id, student_id),
    )
    list_courses = []
    for x in range(len(data)):
        owner = TeacherShow.read_from_query_result(*data[x][8:])
        course = CourseShow.read_from_query_result(*data[x][:8], teacher=owner)
        list_courses.append(course)
    return list_courses


def get_course_by_id(course_id):
    data_sections = read_query(
        "select id,title from sections where courses_id=?", (course_id,)
    )
    list_sections = [
        Section.read_from_query_result(*row, content=None) for row in data_sections
    ]
    for x in list_sections:
        data_content = read_query(
            "select c.id,c.title,c.description,c.content_types_id from content c join sections s on s.id=c.sections_id where s.title=?",
            (x.title,),
        )
        list_content = [Content.read_from_query_result(*row) for row in data_content]
        x.content = list_content
    data_course = read_query(
        "select c.id,c.title,c.description,c.objectives,c.premium,round(sum(r.rating)/count(r.id),2) as rating,c.price,group_concat(distinct t.name) as tags,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id where c.id=? group by c.id",
        (course_id,),
    )
    if data_course == []:
        return "Not found"
    owner = TeacherShow.read_from_query_result(*data_course[0][8:])
    course = CourseShowId.read_from_query_result(
        *data_course[0][:8], teacher=owner, sections=list_sections
    )

    return course


def get_students_courses(student_id):
    courses = read_query(
        "select group_concat(distinct courses_id) from users_has_courses where users_id=? group by users_id",
        (student_id,),
    )
    list_courses = []
    if courses == []:
        return []
    for x in courses[0]:
        data_sections = read_query(
            "select id,title from sections where courses_id=?", (x,)
        )
        list_sections = [
            Section.read_from_query_result(*row, content=None) for row in data_sections
        ]
        for j in list_sections:
            data_content = read_query(
                "select c.id,c.title,c.description,c.content_types_id from content c join sections s on s.id=c.sections_id where s.title=?",
                (j.title,),
            )
            list_content = [
                Content.read_from_query_result(*row) for row in data_content
            ]
            j.content = list_content
        data_course = read_query(
            "select c.id,c.title,c.description,c.objectives,c.premium,round(sum(r.rating)/count(r.id),2) as rating,c.price,group_concat(distinct t.name) as tags,ifnull(round((count(distinct us.sections_id)/count(distinct s.id))*100),0) as progress,uc.subscriptions_id,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id left join sections s on s.courses_id=c.id left join sections se on se.courses_id=c.id left join users_has_sections us on us.sections_id=se.id left join users_has_courses uc on uc.courses_id=c.id where us.users_id=?  and uc.users_id=? and c.id=? group by c.id",
            (student_id, student_id, x),
        )
        if data_course == []:
            return "Not found"
        owner = TeacherShow.read_from_query_result(*data_course[0][10:])
        course = CoursesShowStudent.read_from_query_result(
            *data_course[0][:10], teacher=owner, sections=list_sections
        )
        list_courses.append(course)

    return list_courses


def get_student_course_by_id(student_id, course_id):
    data_sections = read_query(
        "select id,title from sections where courses_id=?", (course_id,)
    )
    list_sections = [
        Section.read_from_query_result(*row, content=None) for row in data_sections
    ]
    for x in list_sections:
        data_content = read_query(
            "select c.id,c.title,c.description,c.content_types_id from content c join sections s on s.id=c.sections_id where s.title=?",
            (x.title,),
        )
        list_content = [Content.read_from_query_result(*row) for row in data_content]
        x.content = list_content
    data_course = read_query(
        "select c.id,c.title,c.description,c.objectives,c.premium,round(sum(r.rating)/count(r.id),2) as rating,c.price,group_concat(distinct t.name) as tags,ifnull(round((count(distinct us.sections_id)/count(distinct s.id))*100),0) as progress,uc.subscriptions_id,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id left join sections s on s.courses_id=c.id left join sections se on se.courses_id=c.id left join users_has_sections us on us.sections_id=se.id left join users_has_courses uc on uc.courses_id=c.id where us.users_id=? and uc.users_id=? and c.id=? group by c.id",
        (student_id, student_id, course_id),
    )
    if data_course == []:
        return "Not found"
    owner = TeacherShow.read_from_query_result(*data_course[0][10:])
    course = CoursesShowStudent.read_from_query_result(
        *data_course[0][:10], teacher=owner, sections=list_sections
    )

    return course


def get_course_by_title(title):
    course_id = read_query("select id from courses where title=?", (title,))
    if course_id == []:
        return "Not found"
    data_sections = read_query(
        "select id,title from sections where courses_id=?", (course_id[0][0],)
    )
    list_sections = [
        Section.read_from_query_result(*row, content=None) for row in data_sections
    ]
    for x in list_sections:
        data_content = read_query(
            "select c.id,c.title,c.description,c.content_types_id from content c join sections s on s.id=c.sections_id where s.title=?",
            (x.title,),
        )
        list_content = [Content.read_from_query_result(*row) for row in data_content]
        x.content = list_content
    data_course = read_query(
        "select c.id,c.title,c.description,c.objectives,c.premium,round(sum(r.rating)/count(r.id),2) as rating,c.price,group_concat(distinct t.name) as tags,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id where c.title=? group by c.id",
        (title,),
    )
    if data_course == []:
        return "Not found"
    owner = TeacherShow.read_from_query_result(*data_course[0][8:])
    course = CourseShowId.read_from_query_result(
        *data_course[0][:8], teacher=owner, sections=list_sections
    )
    return course


def create_course(course: CourseCreate, owner):
    if course.premium == True:
        course.premium = 1
    else:
        course.premium = 0
    list_of_tags = []
    for x in course.tags:
        data = read_query("select id from tags where name=?", (x,))
        if data==[]:
            return f"Tag {x} doesn't exist"
        list_of_tags.append(data[0][0])
    course_id = insert_query(
        "insert into courses(title,description,objectives,premium,active,owner,price,course_picture) values(?,?,?,?,?,?,?,?)",
        (
            course.title,
            course.description,
            course.objectives,
            course.premium,
            1,
            owner,
            course.price,
            course.course_pic,
        ),
    )
    for x in list_of_tags:
        insert_query(
            "insert into tags_has_courses(tags_id,courses_id) values(?,?)",
            (x, course_id),
        )

