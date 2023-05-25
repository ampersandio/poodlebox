from api.data.database import read_query, insert_query
from api.data.models import User, StudentRegistration, TeacherRegistration
import random
from api.services import courses


def get_user(email: str) -> User | None:
    user_data = read_query('SELECT * FROM users WHERE email=?', (email,))

    if not user_data:
        return None
    
    user = User.from_query(*user_data[0])
    return user


def register_student(student_info: StudentRegistration) -> None:
    insert_query('INSERT INTO users(email, first_name, last_name, password, date_of_birth, verified_email, role, disabled) VALUES(?,?,?,?,?,?,?,?);',(
        student_info.email,
        student_info.first_name,
        student_info.last_name,
        student_info.password,
        student_info.date_of_birth,
        False,
        1,
        False
        )
    )


def register_teacher(teacher_info: TeacherRegistration) -> None:
    insert_query('INSERT INTO users(email, first_name, last_name, password, phone_number, date_of_birth, verified_email, approved, role, linked_in_profile, disabled) VALUES(?,?,?,?,?,?,?,?,?,?,?)', (
        teacher_info.email,
        teacher_info.first_name,
        teacher_info.last_name,
        teacher_info.password,
        teacher_info.phone_number,
        teacher_info.date_of_birth,
        False,
        False,
        2,
        teacher_info.linked_in_profile,
        False
        )
    )

def view_add(users_id):
    tags_with_highest_interest=read_query("select group_concat(distinct tags_id) from interests where users_id=? group by tags_id order by relevance desc limit 3",(users_id,))
    print(tags_with_highest_interest)
    if tags_with_highest_interest==[]:
        tags_with_highest_interest=read_query("select group_concat(distinct tags_id) from interests group by tags_id order by relevance desc limit 3")
        tag=random.choice(tags_with_highest_interest[0])
        courses_with_this_tag=read_query("select group_concat(distinct courses_id) from tags_has_courses where tags_id=? group by courses_id",(tag,))
        course=random.choice(courses_with_this_tag[0])
        return courses.get_course_by_id(course)
    tag=random.choice(tags_with_highest_interest[0])
    courses_with_this_tag=read_query("select group_concat(distinct courses_id) from tags_has_courses where tags_id=? and courses_id not in (select courses_id from users_has_courses where users_id=?) group by courses_id",(tag,users_id))
    course=random.choice(courses_with_this_tag[0])
    return courses.get_course_by_id(course)

def get_user_by_id(user_id) -> User | None:
    user_data = read_query('SELECT * FROM users WHERE id=?;', (user_id,))

    if not user_data:
        return None
    
    user = User.from_query(*user_data[0])
    return user
