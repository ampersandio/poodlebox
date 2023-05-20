from api.data.database import read_query, insert_query, update_query
from api.data.models import Subscription, Student
from api.services.courses import get_course_by_id


def get_students_courses_id(student_id):
    data = read_query(
        "select group_concat(distinct courses_id) from users_has_courses where users_id=? group by users_id",
        (student_id,),
    )
    courses_ids = [x for x in data[0].split(",")]
    return courses_ids


def enroll_in_course(student_id, course_id, subscription: Subscription):
    course = get_course_by_id(course_id)
    data = read_query(
        "select subscriptions_id from users_has_courses where users_id=? and courses_id=?",
        (student_id, course_id),
    )
    number_subs = read_query(
        "select count(distinct uc.courses_id) from users_has_courses uc join courses c on c.id=uc.courses_id and c.premium=1 where uc.users_id=?",
        (student_id,),
    )
    if data == [] and subscription.enroll == True and course.premium is False:
        insert_query(
            "insert into users_has_courses(users_id,courses_id,scubscriptions_id) values(?,?,?)",
            (student_id, course_id, 2),
        )
        return "Request sent"
    elif (
        data == []
        and subscription.enroll == True
        and number_subs[0][0] == 5
        and course.premium is True
    ):
        return "You can't enroll in more premium courses"
    elif (
        data == []
        and subscription.enroll == True
        and number_subs[0][0] < 5
        and course.premium is True
    ):
        insert_query(
            "insert into users_has_courses(users_id,courses_id,scubscriptions_id) values(?,?,?)",
            (student_id, course_id, 2),
        )
        return "Request sent"
    elif data == [] and subscription.enroll == False:
        return "Nothing to update"
    elif data != [] and subscription.enroll == False:
        update_query(
            "update users_has_courses set subscriptions_id=? where courses_id=? and users_id=?",
            (3, course_id, student_id),
        )
    elif data != [] and subscription.enroll == True and data[0][0] in [1, 2]:
        return "Nothing to update"
    elif (
        data != []
        and subscription.enroll == True
        and data[0][0] == 3
        and course.premium is False
    ):
        update_query(
            "update users_has_courses set subscriptions_id=? where courses_id=? and users_id=?",
            (2, course_id, student_id),
        )
        return "Request sent"
    elif (
        data != []
        and subscription.enroll == True
        and data[0][0] == 3
        and course.premium is True
        and number_subs[0][0] == 5
    ):
        return "You can't enroll in more premium courses"
    elif (
        data != []
        and subscription.enroll == True
        and data[0][0] == 3
        and course.premium is True
        and number_subs[0][0] < 5
    ):
        update_query(
            "update users_has_courses set subscriptions_id=? where courses_id=? and users_id=?",
            (2, course_id, student_id),
        )
        return "Request sent"


def get_profile(student_id):
    data = read_query(
        "select u.id,u.first_name,u.last_name,u.email,u.verified_email,u.date_of_birth,count(distinct uc.courses_id),count(distinct uco.courses_id),count(distinct ucou.courses_id),count(distinct ucour.courses_id) from users u left join users_has_courses uc on u.id=uc.users_id left join users_has_courses uco on u.id=uco.users_id and uco.subscriptions_id=2 left join users_has_courses ucou on u.id=ucou.users_id and ucou.subscriptions_id=1 left join users_has_courses ucour on u.id=ucour.users_id and ucour.subscriptions_id= 3 where u.id=?",
        (student_id,),
    )
    return (Student.read_from_query_result(*row) for row in data)


def change_password(student_id, new_pass):
    update_query("update users set password=? where id=?", (new_pass, student_id))
