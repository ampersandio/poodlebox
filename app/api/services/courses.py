from api.data.database import read_query, insert_query, update_query, delete_query, multiple_query
from typing import Callable
import api.utils.constants as constants
from mariadb import IntegrityError
from api.data.models import (
    SubscriptionStatus,
    TeacherShow,
    CourseShow,
    Section,
    SectionCreate,
    Content,
    ContentCreate,
    Course,
    CoursesShowStudent,
    CourseCreate,
    CourseShow,
    User,
    PendingEnrollment,
    NicePendingEnrollment,
    CourseEdit
)
from api.data import database

def get_courses_anonymous(db=None):
    '''Get all the courses for a user that doesn't have an account'''
    if db is None:
        db=database.read_query
    data = db(
        "select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0) as rating,c.price,group_concat(distinct t.name) as tags,c.course_picture,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id where c.premium=0 group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile,c.premium,u.id"
    )
    list_courses = []
    for x in range(len(data)):
        owner = TeacherShow.read_from_query_result(*data[x][9:])
        course = CourseShow.read_from_query_result(*data[x][:9], teacher=owner)
        list_courses.append(course)
    return list_courses


def get_courses_teacher(db=None):
    '''Get all the courses in the database'''
    if db is None:
        db=database.read_query
    data = db(
        "select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0) as rating,c.price,group_concat(distinct t.name) as tags,c.course_picture,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile,c.premium,u.id"
    )
    list_courses = []
    for x in range(len(data)):
        owner = TeacherShow.read_from_query_result(*data[x][9:])
        course = CourseShow.read_from_query_result(*data[x][:9], teacher=owner)
        list_courses.append(course)
    return list_courses


def get_courses_student(student_id,db=None):
    '''Get all the courses in the system with the one's that match 
    the tags of the courses the student's already been enrolled in being at the top,
    second are the courses that don't match the tags but the student's never been 
    enrolled in and at the bottom are the ones the student has been enrolled in'''
    if db is None:
        db=database.read_query
    data = db(
        "select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0) as rating,c.price,group_concat(distinct t.name) as tags,c.course_picture,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id where t.name in (select t.name from tags t join interests i on t.id=i.tags_id where i.users_id=?) and c.id not in (select c.id from courses c left join users_has_courses uc on c.id=uc.courses_id where uc.users_id=?) group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile,u.id,c.premium  union select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0) as rating,c.price,group_concat(distinct t.name) as tags,c.course_picture,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id left join users_has_courses uc on uc.courses_id=c.id where t.name not in (select t.name from tags t join interests i on t.id=i.tags_id where i.users_id=?) and c.id not in (select c.id from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id where t.name in (select t.name from tags t join interests i on t.id=i.tags_id where i.users_id=?) and c.id not in (select c.id from courses c left join users_has_courses uc on c.id=uc.courses_id where uc.users_id=?) group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile,u.id,c.premium )  group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile,c.id,c.premium,u.id union select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0)  as rating,c.price,group_concat(distinct t.name) as tags,c.course_picture,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id where c.id in (select c.id from courses c join users_has_courses uc on c.id=uc.courses_id where uc.users_id=?) group by c.id,c.title,c.description,c.objectives,c.price,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile,u.id,c.premium",
        (student_id, student_id, student_id, student_id, student_id, student_id),
    )
    list_courses = []
    for x in range(len(data)):
        owner = TeacherShow.read_from_query_result(*data[x][9:])
        course = CourseShow.read_from_query_result(*data[x][:9], teacher=owner)
        list_courses.append(course)
    return list_courses


def get_course_by_id(course_id: int,db=None):
    '''Get a course by its id'''
    if db is None:
        db=database.read_query
    data_course = db(
        "select c.id,c.title,c.description,c.objectives,c.premium,round(sum(r.rating)/count(r.id),2) as rating,c.price,group_concat(distinct t.name) as tags,c.course_picture,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id left join users u on u.id=c.owner left join tags_has_courses ta on ta.courses_id=c.id left join tags t on t.id=ta.tags_id where c.id=?",
        (course_id,),
    )
    if data_course[0][0] == None:
        return None
    owner = TeacherShow.read_from_query_result(*data_course[0][9:])
    course = CourseShow.read_from_query_result(
        *data_course[0][:9], teacher=owner
    )

    return course


def get_students_courses(student_id,db=None):
        '''Get all the courses a student's been enrolled in'''
        if db is None:
            db=database.read_query
        data_course = db(
            "select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0) as rating,c.price,group_concat(distinct t.name) as tags,ifnull(round((count(distinct us.sections_id)/count(distinct s.id))*100),0) as progress,uc.subscriptions_id,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id join users u on u.id=c.owner join tags_has_courses ta on ta.courses_id=c.id join tags t on t.id=ta.tags_id left join sections s on s.courses_id=c.id left join sections se on se.courses_id=c.id left join users_has_sections us on us.sections_id=se.id  and us.users_id=? join users_has_courses uc on uc.courses_id=c.id and uc.users_id=? group by c.id",
            (student_id, student_id),
        )
        if data_course==[]:
            return []
        list_courses=[]
        # print(data_course[0][:10])
        for x in data_course:
         owner = TeacherShow.read_from_query_result(*x[10:])
         course = CoursesShowStudent.read_from_query_result(
            *x[:10], teacher=owner
        )
         list_courses.append(course)

        return list_courses


def get_student_course_by_id(student_id, course_id,db=None):
    '''Get a course a student's been enrolled in by its id'''
    if db is None:
        db=database.read_query
    data_course = db(
        "select c.id,c.title,c.description,c.objectives,c.premium,ifnull(round(sum(r.rating)/count(r.id),2),0) as rating,c.price,group_concat(distinct t.name) as tags,ifnull(round((count(distinct us.sections_id)/count(distinct s.id))*100),0) as progress,uc.subscriptions_id,u.id,u.first_name,u.last_name,u.phone_number,u.email,u.linked_in_profile from courses c left join reviews r on r.courses_id=c.id join users u on u.id=c.owner join tags_has_courses ta on ta.courses_id=c.id join tags t on t.id=ta.tags_id left join sections s on s.courses_id=c.id left join sections se on se.courses_id=c.id left join users_has_sections us on us.sections_id=se.id  and us.users_id=?  join users_has_courses uc on uc.courses_id=c.id and uc.users_id=? where c.id=?",
        (student_id, student_id, course_id),
    )
    owner = TeacherShow.read_from_query_result(*data_course[0][10:])
    course = CoursesShowStudent.read_from_query_result(*data_course[0][:10], teacher=owner)

    return course


def create_course(course: CourseCreate, owner):
    '''Create a course'''
    if course.premium == True:
        course.premium = 1
    else:
        course.premium = 0
    list_of_tags = []

    for x in course.tags:
        data = read_query("select id from tags where name=?", (x,))
        if data == []:
            id=insert_query("insert into tags(name) values(?)",(x,))
            list_of_tags.append(id)
        else:
            list_of_tags.append(data[0][0])

    try:
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
                course.course_picture,
            ),
        )
    except:
        raise IntegrityError

    for x in list_of_tags:
        insert_query(
            "insert into tags_has_courses(tags_id,courses_id) values(?,?)",
            (x, course_id),
        )


def edit(course_id: int, new_information: CourseEdit) -> None:
    '''
    Edit course, setting new tags, objectives, course picture
    '''
    params = [course_id]
    tag_queries = ''
    for tag in new_information.tags:
        tag_queries += 'INSERT INTO tags_has_courses(courses_id, tags_id) VALUES(?, (SELECT id FROM tags WHERE name = ?)); '
        params.append(course_id)
        params.append(tag)

    params.append(new_information.objectives)
    params.append(new_information.course_picture)
    params.append(course_id)

    multiple_query('DELETE FROM tags_has_courses WHERE courses_id = ?; ' +
                 tag_queries +
                 'UPDATE courses SET objectives = ?, course_picture = ? WHERE id = ?',
                 params)


def add_course_photo(course_picture: str, course_id: int, get_course_func: Callable = None):
    '''Add a photo for a particular course'''
    if get_course_func == None:
        get_course_func = get_course_by_id

    course = get_course_func(course_id)
    if course:
        insert_query("update courses set course_picture = ? where id = ?", (course_picture, course_id,))
    else:
        return None
    

def get_section_by_id(section_id: int) -> Section:
    section_data = read_query(
        "select id, title from sections where id = ?;", (section_id,)
    )
    content_data = read_query(
        "select c.id, c.title, c.description, ct.type, link from content as c join content_types as ct on c.content_types_id = ct.id where sections_id = ?;",
        (section_id,),
    )
    content = [Content.read_from_query_result(*row) for row in content_data]

    if section_data:
        section_id, section_title = section_data[0]
        section = Section.read_from_query_result(
            id=section_id, title=section_title, content=content
        )
    else:
        return None
    return section


def create_section(course_id: int, section: SectionCreate):
    last_section_id = insert_section(section.title, course_id)

    if section.content:
        for content in section.content:
            content_type_id = get_content_type_id(content.content_type)

            if content_type_id:
                insert_content(content.title, content.description, content_type_id, last_section_id)
            else:
                last_content_type_id = insert_content_type(content.content_type)
                insert_content(content.title, content.description, last_content_type_id, last_section_id)

    return get_section_by_id(last_section_id)


def insert_section(title: str, course_id: int, query_func: Callable = None) -> int:
    if query_func == None:
        query_func = insert_query

    query = "INSERT INTO sections (title, courses_id) VALUES (?, ?);"
    section_id = query_func(query, (title, course_id))
    return section_id


def get_content_type_id(content_type: str) -> int:
    query = "SELECT id FROM content_types WHERE type = ?;"
    result = read_query(query, (content_type,))
    if result:
        return result[0][0]
    

def insert_content(title: str, description: str, content_type_id: int, section_id: int, link: str | None=None):
    query = "INSERT INTO content (title, description, content_types_id, sections_id, link) VALUES (?, ?, ?, ?, ?);"
    insert_query(query, (title, description, content_type_id, section_id, link))


def insert_content_type(content_type: str, query_func: Callable = None) -> int:
    if query_func == None:
        query_func = insert_query

    query = "INSERT INTO content_types (type) VALUES (?);"
    content_type_id = query_func(query, (content_type,))
    return content_type_id


def update_section(section_id: int, new_section: SectionCreate):
    last_section_id = update_query(
        "update sections set title = ? where id = ?;",
        (
            new_section.title,
            section_id,
        ),
    )

    return get_section_by_id(last_section_id)


def get_content_by_id(content_id: int) -> Content:

    content_data = read_query(
        "select id, title, description, content_types_id, link from content where id = ?;",
        (content_id,),
    )
    
    content = [Content.read_from_query_result(*row) for row in content_data]

    return content


def add_content(section_id: int, content: ContentCreate) -> Content:

    content_type_id = read_query("select id from content_types where type = ?;", (content.content_type,))

    if not content_type_id:
        content_type_id = insert_content_type(content.content_type)
    else:
        content_type_id = content_type_id[0][0]

    last_content_id = insert_content(content.title, content.description, content_type_id, section_id, content.link)
    
    return get_content_by_id(last_content_id)


def get_most_popular(role: str | None = None):

    if role is None:
        query = "select c.id, c.title, c.description, c.objectives, c.premium, c.active, c.owner, c.price, c.course_picture from courses as c join users_has_courses as u on c.id = u.courses_id where c.premium = 0 group by c.id order by count(u.users_id) desc limit 4;"
    else:
        query = "select c.id, c.title, c.description, c.objectives, c.premium, c.active, c.owner, c.price, c.course_picture from courses as c join users_has_courses as u on c.id = u.courses_id group by c.id order by count(u.users_id) desc limit 4;"

    courses_data = read_query(query)

    courses = [Course.read_from_query_result(*data) for data in courses_data]

    return courses


def get_course_students(course_id: int):

    data = read_query(
        "select u.* from courses as c join users_has_courses as uc on c.id = uc.courses_id join users as u on uc.users_id = u.id where c.id = ?;",
        (course_id,),
    )
    if data:
        students = [User.from_query(*row) for row in data]
        return students
    else:
        return None


def delete_section(section_id: int, query_func: Callable = None, get_section_by_id_func: Callable = None):
    if query_func == None:
        query_func = update_query
    
    if get_section_by_id_func == None:
        get_section_by_id_func = get_section_by_id

    section = get_section_by_id_func(section_id)
    if section:
        query_func("delete from sections where id = ?;", (section_id,))
    else:
        return None


def section_update(section_id: int, section: SectionCreate):
    update_query(
        "update sections set title = ?, content = ? where id = ?;",
        (
            section.title,
            section.content,
            section_id,
        ),
    )


def visit_section(user_id: int, section_id: int):
    visited_section = read_query("select * from users_has_sections where users_id = ? and sections_id = ?;", (user_id, section_id,))
    
    if not visited_section:
        last_section = insert_query("insert into users_has_sections(users_id,sections_id) values(?,?);",(user_id,section_id,))
        return last_section
    else:
        return None


def n_sections_by_course_id(course_id: int) -> int:
    data = read_query("select c.title,c.id as course_id, count(*) as number_of_sections from sections as s join courses as c on s.courses_id = c.id where c.id = ? group by courses_id;",(course_id,))

    return data[0][2]


def n_visited_sections(user_id: int, course_id: int) -> int:
    data = read_query("select count(*) from users_has_sections as us join sections as s on us.sections_id = s.id where us.users_id = ? and s.courses_id = ?;", (user_id,course_id,))

    return data[0][0]


def change_subscription(subscription: int, user_id: int, course_id: int):

    subscription_data = read_query("select * from users_has_courses where users_id = ? and courses_id = ?;", (user_id, course_id,))
    subscription_status = next((SubscriptionStatus.from_query(*data) for data in subscription_data),None)

    if subscription_status.subscription == "2":
        return None
    else:
        return update_query("update users_has_courses set subscriptions_id = ? where users_id = ? and courses_id = ?;", (subscription, user_id, course_id,))


def get_course_sections(course_id:int):
    data_sections = read_query(
        "select id,title from sections where courses_id=?", (course_id,)
    )
    list_sections = [Section.read_from_query_result(*row, content=None) for row in data_sections]

    for x in list_sections:
        data_content = read_query(
            "select c.id,c.title,c.description,c.content_types_id,link from content c join sections s on s.id=c.sections_id where s.title=?",
            (x.title,),
        )
        list_content = [Content.read_from_query_result(*row) for row in data_content]
        x.content = list_content

    return(list_sections)


def leave_review(user_id: int, course_id: int, rating: float, description: str) -> bool:
    try:
        insert_query('INSERT INTO reviews(users_id, courses_id, rating, description) VALUES(?,?,?,?)', (user_id, course_id, rating, description))
        return True
    except IntegrityError:
        return False
    

def deactivate_course(course_id: int, query_func: Callable = None) -> bool:
    if query_func == None:
        query_func = update_query

    updated = query_func('UPDATE courses SET active=0 WHERE id=?', (course_id,))
    return bool(updated)


def activate_course(course_id: int, query_func: Callable = None) -> bool:
    if query_func == None:
        query_func = update_query

    updated = query_func('UPDATE courses SET active=1 WHERE id=?', (course_id,))
    return bool(updated)


def get_course_owner(course_id: int, query_func: Callable = None) -> int:
    if query_func == None:
        query_func = read_query

    data = query_func('SELECT owner FROM courses WHERE id=?', (course_id,))
    owner = data[0][0]

    return owner


def get_pending_enrollments(owner_id: int) -> list[PendingEnrollment] | None:
    data = read_query('SELECT users_id, courses_id FROM users_has_courses WHERE subscriptions_id = 2 AND courses_id IN (SELECT id FROM courses WHERE owner = ?)', (owner_id,))

    pending_enrollments = [PendingEnrollment.from_query(*row) for row in data]
    if not pending_enrollments:
        return None
    
    return pending_enrollments


def get_nice_pending_enrollments(owner_id: int) -> list[PendingEnrollment] | None:
    data = read_query('SELECT u.id,u.first_name,u.last_name,c.id,c.title from users as u join users_has_courses as uc on u.id = uc.users_id join courses as c on c.id = uc.courses_id where uc.subscriptions_id = 2 and c.id in (SELECT id FROM courses WHERE owner = 2);'), (owner_id,) 
    pending_enrollments = [NicePendingEnrollment.from_query(*row) for row in data[0]]

    print(pending_enrollments)
    if not pending_enrollments:
        return None
    
    return pending_enrollments


def approve_enrollment(user_id: int, course_id: int, query_func: Callable = None) -> bool:
    if query_func == None:
        query_func = update_query

    enrolled = query_func('UPDATE users_has_courses SET subscriptions_id = 1 WHERE users_id=? AND courses_id=?', (user_id, course_id))
    return bool(enrolled)


def reject_enrollment(user_id: int, course_id: int, query_func: Callable = None) -> bool:
    if query_func == None:
        query_func = delete_query

    rejected = query_func('DELETE FROM users_has_courses WHERE users_id=? AND courses_id=?', (user_id, course_id))
    return bool(rejected)


def check_ownership(user_id: int, course_id: int, query_func: Callable = None) -> bool:
    if query_func == None:
        query_func = read_query

    owner_id = query_func('SELECT owner FROM courses WHERE id = ?', (course_id,))[0][0]

    if user_id != owner_id:
        return False
    
    return True