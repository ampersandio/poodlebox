from api.data.database import read_query, insert_query, update_query
from api.data.models import User


def student_status(student_id:int, disabled:bool):
    if disabled:
        update_query("update users set disabled = 1 where id = ?;", (student_id,))
    else:
        update_query("update users set disabled = 0 where id = ?;", (student_id,))

def course_status(course_id:int, disabled:bool):
    if disabled:
        update_query("update courses set active = 1 where id = ?;", (course_id,))
    else:
        update_query("update courses set active = 0 where id = ?;", (course_id,))


def remove_student(course_id:int, student_id:int):
    update_query("update users_has_courses set subscriptions_id = 3 where courses_id = ? and users_id = ?;", (course_id, student_id,))


def pending_registrations():
    data = read_query("select * from users where role = 2 and approved = 0 and verified_email = 1;")
    users = [User.from_query(*row) for row in data]

    return users


def approve_registration(teacher_id:int):
    update_query("update users set approved = 1 where id = ?;", (teacher_id,))

def search_courses():
    # search through courses filtered by teacher and/or by student
    pass

def traceback_ratings():
    # endpoint 
    pass
