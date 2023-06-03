import uuid
from api.data.database import read_query, insert_query
from api.data.models import Certificate


def create_certificate(student_id, course_id, date):
    """Create a certificate for a particular course"""
    certificate_id = uuid.uuid1()
    read_query(
        "insert into certificates(id,users_id,courses_id,issued_date) values(?,?,?,?)",
        (certificate_id, student_id, course_id, date),
    )


def get_certificates(student_id):
    """Get all the certificates of a user"""
    data = read_query(
        "select id,users_id,courses_id,issued_date from certificates where users_id=? group by id",
        (student_id,),
    )
    if data == []:
        return []
    return (Certificate.read_from_query_result(*row) for row in data)


def get_certificate_by_course(student_id, course_id):
    """Get a certificate by its course's id"""
    data = read_query(
        "select id,users_id,courses_id,issued_date from certificates where users_id=? and courses_id=? group by id",
        (student_id, course_id),
    )
    if data == []:
        return None
    return (Certificate.read_from_query_result(*row) for row in data)


def verify_certificate(id):
    """Verify a certificate with it's id"""
    data = read_query("select users_id from certificates where id=?", (id,))
    if data == []:
        return False
    return True
