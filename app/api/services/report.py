from data.database import read_query
from data.models import (
    UserForCourse,
    CourseForTeachersReport,
    TeachersReport
)

#     id: int
#     name: str
#     role: str
#     completed: int
#     review: int | None


def get_users_for_course(course_id: int) -> list[UserForCourse] | None:
    data = read_query('SELECT u.id, CONCAT(u.first_name, " ", u.last_name), u.role, COUNT(com_s.com_id)/COUNT(cou_s.sec_id), r.rating '+
                      'FROM users u JOIN users_has_courses uhc ON u.id = uhc.users_id WHERE uhc.courses_id = ? '+
                      'JOIN (SELECT uhs.sections_id, uhs.users_id AS com_id FROM users_has_sections uhs JOIN users u ON uhs.users_id = u.id WHERE uhs.sections_id IN (SELECT s.id FROM sections s WHERE s.courses_id = ?)) AS com_s ON com_s.users_id = u.id '+
                      'JOIN (SELECT s.id, AS sec_id, uhs.id AS u_id FROM sections s JOIN courses c ON s.courses_id = c.id WHERE c.id = ? JOIN users_has_sections uhs ON s.id = uhs.sections_id) AS cou_s ON cou_s.u_id = u.id '+
                      'JOIN (SELECT r.rating, r.users_id FROM reviews r JOIN courses c ON c.id = r.courses_id WHERE c.id = ?) AS r ON r.users_id = u.id '+
                      'GROUP BY u.id, com_s.com_id, cou_s.sec_id'
                      )