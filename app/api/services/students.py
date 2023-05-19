from api.data.database import read_query
def get_students_courses_id(student_id):
    data=read_query("select group_concat(distinct courses_id) from users_has_courses where users_id=? group by users_id",(student_id,))
    courses_ids=[x for x in data[0].split(",")]
    return courses_ids
