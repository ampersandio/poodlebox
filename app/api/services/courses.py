from api.data.database import read_query, insert_query, update_query
from api.data.models import (
    TeacherShow,
    CourseShow,
    Section,
    SectionCreate,
    Content,
    ContentCreate,
    Course,
    CourseShowId,
    CoursesShowStudent,
    CourseCreate,
    CourseShow,
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


def get_course_by_id(course_id:int):
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


def get_section_by_id(section_id:int) -> Section:
    section_data = read_query("select id, title from sections where id = ?;", (section_id,))
    content_data = read_query("select c.id, c.title, c.description, ct.type from content as c join content_types as ct on c.content_types_id = ct.id where sections_id = ?;", (section_id,))
    content = [Content.read_from_query_result(*row) for row in content_data]

    if section_data:
        section_id, section_title = section_data[0]
        section = Section.read_from_query_result(id=section_id, title=section_title, content=content)

    return section


def create_section(course_id:int, section: SectionCreate):

    last_section_id = insert_query("insert into sections(title,courses_id) values(?,?);", (section.title,course_id,) )

    if section.content:
        for content in section.content:
            content_type_id = read_query("select id from content_types where type = ?;", (content.content_type,))[0][0]
            if content_type_id:
                insert_query("insert into content(title,description,content_types_id,sections_id) values(?,?,?,?);", (content.title,content.description,content_type_id,last_section_id))
            else:
                last_content_type_id = insert_query("insert into content_types(type) values(?);", (content.content_type,))
                insert_query("insert into content(title,description,content_types_id,sections_id) values(?,?,?,?);", (content.title,content.description,last_content_type_id,last_section_id))

    return get_section_by_id(last_section_id)


def get_content_by_id(content_id:int) -> Content:
    content_data = read_query("select id, title, description, content_types_id from content where id = ?;", (content_id,))
    content = [(Content.read_from_query_result(*row) for row in content_data)]

    return content


def add_content(section_id: int, content: ContentCreate) -> Content:
    content_type_id = read_query("select id from content_types where type = ?;", (content.content_type,))[0][0]
    
    if not content_type_id:
        last_content_type_id = insert_query("insert into content_types(type) values(?);", (content.content_type,))
        content_type_id = last_content_type_id
        
    last_content_id = insert_query("insert into content(title, description, content_types_id, sections_id) values(?,?,?,?);",(content.title, content.description, content_type_id, section_id))

    return get_content_by_id(last_content_id)
    

def get_most_popular(role: str | None = None):
    if role is None:
        query = "select c.id, c.title, c.description, c.objectives, c.premium, c.active, c.owner, c.price, c.course_picture from courses as c join users_has_courses as u on c.id = u.courses_id where c.premium = 0 group by c.id order by count(u.users_id) desc limit 3;"
    else:
        query = "select c.id, c.title, c.description, c.objectives, c.premium, c.active, c.owner, c.price, c.course_picture from courses as c join users_has_courses as u on c.id = u.courses_id group by c.id order by count(u.users_id) desc limit 3;"

    courses_data = read_query(query)
    courses = [Course.read_from_query_result(*data) for data in courses_data]
    
    return courses


def visited_section(user_id:int,section_id:int):
    last_section = insert_query("insert into users_has_sections(users_id,sections_id) values(?,?);", (user_id,section_id))
    
def n_sections_by_course_id(course_id:int) -> int:
    return read_query("select c.title,c.id as course_id, count(*) as number_of_sections from sections as s join courses as c on s.courses_id = c.id where c.id = ? group by courses_id;", (course_id,))

def n_visited_sections(user_id:int, course_id:int) -> int:
    return read_query("select count(*) from users_has_sections as us join sections as s on us.sections_id = s.id where us.users_id = ? and s.courses_id = ?;", (user_id,course_id,))

def change_subscription(subscription:int, user_id:int, course_id:int):
    update_query("update users_has_courses set subscriptions = ? where users_id = ? and courses_id = ?;", (subscription,user_id,course_id))