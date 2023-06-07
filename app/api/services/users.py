from api.data.database import read_query, insert_query
from api.data.models import User, StudentRegistration, TeacherRegistration, EditTeacherProfile
from pydantic import ValidationError
import random
from api.services import courses, authorization


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


def view_ad(users_id):
    '''Generate a random course ad for a user that has a random tag from the 3 most relevant tags for this user'''
    tags_with_highest_interest=read_query("select distinct tags_id from interests where users_id=? order by relevance desc limit 3",(users_id,))
    if tags_with_highest_interest==[]:
        tags_with_highest_interest=read_query("select distinct tags_id from interests group by tags_id order by relevance desc limit 3")
        if tags_with_highest_interest==[]:
            return None
        list_tags=[]
        for x in tags_with_highest_interest:
            list_tags.append(int(x[0]))
        tag=random.choice(list_tags)
        courses_with_this_tag=read_query("select group_concat(distinct courses_id) from tags_has_courses where tags_id=?",(tag,))
        if courses_with_this_tag==[(None,)]:
            return None
        list_courses=[int(x) for x in courses_with_this_tag[0][0].split(",")]
        course=random.choice(list_courses)
    list_tags=[]
    for x in tags_with_highest_interest:
            list_tags.append(int(x[0]))
    tag=random.choice(list_tags)
    courses_with_this_tag=read_query("select group_concat(distinct courses_id) from tags_has_courses where tags_id=? and courses_id not in (select courses_id from users_has_courses where users_id=?)",(tag,users_id))
    if courses_with_this_tag==[(None,)]:
        course_data=read_query("select group_concat(distinct courses_id) from tags_has_courses where courses_id not in (select courses_id from users_has_courses where users_id=?)",(users_id,))
        if course_data==[(None,)]:
            return None
        else:
            list_courses=[int(x) for x in course_data[0][0].split(",")]
            course=random.choice(list_courses)
            return courses.get_course_by_id(course)
    list_courses=[int(x) for x in courses_with_this_tag[0][0].split(",")]
    course=random.choice(list_courses)
    return courses.get_course_by_id(course)


def get_user_by_id(user_id) -> User | None:
    user_data = read_query('SELECT * FROM users WHERE id=?;', (user_id,))

    if not user_data:
        return None
    
    user = User.from_query(*user_data[0])
    return user


def edit_teacher_profile(new_information: EditTeacherProfile, user: User) -> None:
    new_hashed_password = authorization.hash_password(new_information.new_password)

    insert_query('UPDATE users SET password=?, phone_number=?, linked_in_profile=?, profile_picture=? WHERE email=?', (
        new_hashed_password, 
        new_information.phone_number, 
        new_information.linked_in_profile, 
        new_information.profile_picture,
        user.email)
        )
