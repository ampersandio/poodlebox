from api.data.models import Subscription, Student

from api.data import database

def get_students_courses_id(student_id,db=None):
    '''Get all the ids of all the courses a student's been enrolled in'''
    if db is None:
        db=database.read_query
    data = db(
        "select group_concat(distinct courses_id) from users_has_courses where users_id=?",
        (student_id,),
    )
    if data==[(None,)]:
        return []
    courses_ids = [int(x) for x in data[0][0].split(",")]
    return courses_ids

def get_students_active_courses(student_id,db=None):
    '''Get all the ids of all the courses a student's currently enrolled in'''
    if db is None:
        db=database.read_query
    data = db(
        "select group_concat(distinct courses_id) from users_has_courses where users_id=? and subscriptions_id=1",
        (student_id,),
    )
    if data==[(None,)]:
        return []
    courses_ids = [int(x) for x in data[0][0].split(",")]
    return courses_ids 


def check_enrollment_status(student_id,course_id,db=None):
    '''Check the enrollment status for a course a student's been enrolled in'''
    if db is None:
        db=database.read_query
        
    data = db(
        "select subscriptions_id from users_has_courses where users_id=? and courses_id=?",
        (student_id, course_id),
    )
    if data==[]:
        return None
    return data[0][0]


def get_students_number_courses_premium(student_id,db=None):
    '''Get the number of premium courses the student is currently enrolled in'''
    if db is None:
        db=database.read_query
    number_subs = db("select count(distinct uc.courses_id) from users_has_courses uc join courses c on c.id=uc.courses_id and c.premium=1 where uc.users_id=? and uc.subscriptions_id=1",
        (student_id,))
    return number_subs[0][0]


def enroll_in_course(student_id: int, course_id:int, subscription: Subscription, expired, db=None):
    '''Change subscriptions status for a course'''
    print("Hello")

    if db is None:
        db=database.insert_query

    if subscription.enroll==True and expired==False:
        db("insert into users_has_courses(users_id,courses_id,subscriptions_id) values(?,?,?)", (student_id, course_id, 2,))
    
    elif subscription.enroll==True and expired==True:
        if db==database.insert_query:
            db=database.update_query
        db("update users_has_courses set subscriptions_id=? where courses_id=? and users_id=?", (2, course_id, student_id,))

    else:
        if db==database.insert_query:
            db=database.update_query
        db("update users_has_courses set subscriptions_id=? where courses_id=? and users_id=?", (3, course_id, student_id,))         




def get_profile(student_id,db=None):
    '''Get the profile of a student'''
    if db is None:
        db=database.read_query
    data = db(
        "select u.id,u.first_name,u.last_name,u.email,u.verified_email,u.date_of_birth,count(distinct uc.courses_id),count(distinct uco.courses_id),count(distinct ucou.courses_id),count(distinct ucour.courses_id) from users u left join users_has_courses uc on u.id=uc.users_id left join users_has_courses uco on u.id=uco.users_id and uco.subscriptions_id=2 left join users_has_courses ucou on u.id=ucou.users_id and ucou.subscriptions_id=1 left join users_has_courses ucour on u.id=ucour.users_id and ucour.subscriptions_id= 3 where u.id=?",
        (student_id,),
    )
    return Student.read_from_query_result(*data[0])


def change_password(student_id, new_pass,db=None):
    '''Change student's password'''
    if db is None:
        db=database.update_query
    db("update users set password=? where id=?", (new_pass, student_id))


def update_interest(student_id: int, course_id: int) -> None:
    database.update_query('UPDATE interests SET relevance = relevance + 1 WHERE users_id=? AND tags_id IN (SELECT tags_id FROM tags_has_courses WHERE courses_id=?)', (student_id, course_id))

