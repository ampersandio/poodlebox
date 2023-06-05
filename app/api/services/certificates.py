import uuid
from api.data import database
from api.data.models import Certificate



def create_certificate(student_id, course_id, date,db=None):
    """Create a certificate for a particular course"""
    if db is None:
        db=database.read_query
    certificate_id = uuid.uuid1()
    db(
        "insert into certificates(id,users_id,courses_id,issued_date) values(?,?,?,?)",
        (certificate_id, student_id, course_id, date),
    )


def get_certificates(student_id,db=None):
    """Get all the certificates of a user"""
    if db is None:
        db=database.read_query
    data = db(
        "select id,users_id,courses_id,issued_date from certificates where users_id=? group by id",
        (student_id,),
    )
    if data == []:
        return []
    return [(Certificate.read_from_query_result(*row) for row in data)]


def get_certificate_by_course(student_id, course_id,db=None):
    """Get a certificate by its course's id"""
    if db is None:
        db=database.read_query
    data = db(
        "select id,users_id,courses_id,issued_date from certificates where users_id=? and courses_id=? group by id",
        (student_id, course_id),
    )
    if data == []:
        return None
    return next((Certificate.read_from_query_result(*row) for row in data),None)


def verify_certificate(id,db=None):
    """Verify a certificate with it's id"""
    if db is None:
        db=database.read_query
    data = db("select users_id from certificates where id=?", (id,))
    if data == []:
        return False
    return True
