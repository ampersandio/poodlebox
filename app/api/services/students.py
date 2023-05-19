from api.data.database import read_query, insert_query, update_query
from api.data.models import Subscription
def get_students_courses_id(student_id):
    data=read_query("select group_concat(distinct courses_id) from users_has_courses where users_id=? group by users_id",(student_id,))
    courses_ids=[x for x in data[0].split(",")]
    return courses_ids


def enroll_in_course(student_id,course_id,subscription:Subscription):
    data=read_query("select subscriptions_id from users_has_courses where users_id=? and courses_id=?",(student_id,course_id))
    if data==[] and subscription.enroll==True:
        insert_query("insert into users_has_courses(users_id,courses_id,scubscriptions_id) values(?,?,?)",(student_id,course_id,2))
        return "Request sent"
    elif data==[] and subscription.enroll==False:
        return "Nothing to update"
    elif data!=[] and subscription.enroll==False:
        update_query("update users_has_courses set subscriptions_id=? where courses_id=? and users_id=?",(3,course_id,student_id))
    elif data!=[] and subscription.enroll==True and data[0][0] in [1,2]:
        return "Nothing to update"
    elif data!=[] and subscription.enroll==True and data[0][0]==3:
        update_query("update users_has_courses set subscriptions_id=? where courses_id=? and users_id=?",(2,course_id,student_id))
        return "Request sent"
