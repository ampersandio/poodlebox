from api.data.database import read_query, insert_query, update_query
from api.data.models import Subscription, Student, Certificate
from api.services.courses import get_course_by_id
from api.utils.utils import enrollment_mail
import uuid

def get_students_courses_id(student_id):
    data = read_query(
        "select group_concat(distinct courses_id) from users_has_courses where users_id=? group by users_id",
        (student_id,),
    )

    courses_ids = [int(x) for x in data[0]]
    return courses_ids


def check_enrollment_status(student_id,course_id):
    data = read_query(
        "select subscriptions_id from users_has_courses where users_id=? and courses_id=?",
        (student_id, course_id),
    )
    if data==[]:
        return "No status"
    return data[0][0]


def get_students_number_courses_premium(student_id):
    number_subs = read_query("select count(distinct uc.courses_id) from users_has_courses uc join courses c on c.id=uc.courses_id and c.premium=1 where uc.users_id=?",
        (student_id,))
    return number_subs[0][0]


def enroll_in_course(student_id: int, course_id:int, subscription: Subscription, expired):
    student = get_profile(student_id)
    course = get_course_by_id(course_id)
    teacher = course.teacher

    send_mail = False

    if subscription.enroll==True and expired==False:
        insert_query("insert into users_has_courses(users_id,courses_id,scubscriptions_id) values(?,?,?)", (student_id, course_id, 2),)
        send_mail = True

    elif subscription.enroll==True and expired==True:
        update_query("update users_has_courses set subscriptions_id=? where courses_id=? and users_id=?", (2, course_id, student_id),)
        send_mail = True

    else:
        update_query("update users_has_courses set subscriptions_id=? where courses_id=? and users_id=?", (3, course_id, student_id))         

    if send_mail:
        enrollment_mail(student,course,teacher)


def get_profile(student_id):
    data = read_query(
        "select u.id,u.first_name,u.last_name,u.email,u.verified_email,u.date_of_birth,count(distinct uc.courses_id),count(distinct uco.courses_id),count(distinct ucou.courses_id),count(distinct ucour.courses_id) from users u left join users_has_courses uc on u.id=uc.users_id left join users_has_courses uco on u.id=uco.users_id and uco.subscriptions_id=2 left join users_has_courses ucou on u.id=ucou.users_id and ucou.subscriptions_id=1 left join users_has_courses ucour on u.id=ucour.users_id and ucour.subscriptions_id= 3 where u.id=?",
        (student_id,),
    )
    return next((Student.read_from_query_result(*row) for row in data), None)


def change_password(student_id, new_pass):
    update_query("update users set password=? where id=?", (new_pass, student_id))



