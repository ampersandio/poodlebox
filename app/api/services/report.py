from api.data.database import read_query
from api.data.models import (
    User,
    CourseUserReview,
    CourseUsersReviews,
    UsersReviewsForCourse,
    TeachersReport
)


def get_teachers_report(teacher: User) -> TeachersReport | None:
    data = read_query(
        'SELECT c.course_id, c.title, cr.total_rating, cu.id as user_id, CONCAT(cu.first_name, " ", cu.last_name) as full_name, cu.email, cu.subscriptions_id, cu.role, IFNULL(com.completed_sections, 0)/t.sections as completed_sections, r.rating, r.description AS review FROM (SELECT c.id course_id, c.title FROM courses c JOIN users u ON c.owner = u.id WHERE u.id = ?) AS c '+
        'JOIN (SELECT uhc.subscriptions_id, uhc.courses_id, u.id, u.first_name, u.last_name, u.email, u.role FROM users_has_courses uhc JOIN users u ON u.id = uhc.users_id WHERE subscriptions_id != 2) AS cu ON cu.courses_id = c.course_id '+
        'LEFT JOIN (SELECT u.id user_id, r.rating, r.courses_id, r.description FROM users u JOIN reviews r ON u.id = r.users_id) as r ON r.courses_id = c.course_id AND r.user_id = cu.id '+
        'JOIN (SELECT c.id course_id, COUNT(s.id) sections FROM sections s JOIN courses c ON s.courses_id = c.id '+
        'GROUP BY c.id) as t ON t.course_id = c.course_id '+
        'LEFT JOIN (SELECT c.id course_id, uhs.users_id, COUNT(uhs.sections_id) completed_sections FROM users_has_sections uhs JOIN sections s ON uhs.sections_id = s.id JOIN courses c ON s.courses_id = c.id '+
        'GROUP BY uhs.users_id, c.id) as com ON com.course_id = c.course_id AND com.users_id = cu.id '+
        'JOIN (SELECT r.courses_id, SUM(r.rating)/(COUNT(r.rating)*10) total_rating FROM reviews r GROUP BY r.courses_id) as cr ON cr.courses_id = c.course_id',
        (teacher.id,)
    )

    if not data:
        return None
    
    courses_users_reviews = [CourseUserReview.from_query(*row) for row in data]
    courses_ids = []
    teachers_report = TeachersReport(
        teacher_id=teacher.id,
        teacher_name=teacher.first_name + teacher.last_name,
        courses_users_reviews=[]
    )
    course_users_reviews = None
    for course_user_review in courses_users_reviews:
        if course_user_review.course_id not in courses_ids:
            courses_ids.append(course_user_review.course_id)
            course_users_reviews = CourseUsersReviews(
                course_id=course_user_review.course_id,
                title=course_user_review.title,
                total_rating=course_user_review.total_rating,
                users_reviews=[]
                )
            teachers_report.courses_users_reviews.append(course_users_reviews)
        course_users_reviews.users_reviews.append(UsersReviewsForCourse.from_CourseUserReview(course_user_review))

    return teachers_report
   
    