import unittest
from api.services import report
from api.data.models import CourseUserReview, UsersReviewsViewForCourse, TeachersReport, CourseViewForReport, User
from datetime import date


FAKE_TEACHER = User(
    id=1,
    email='teacher@gmail.com',
    first_name='pepa',
    last_name='old',
    hashed_password='HASHED_PASSWORD',
    phone_number='123123123',
    date_of_birth=date.today(),
    verified_email=True,
    approved=True,
    role='teacher',
    linked_in_profile='linkedin.com',
    disabled=False,
    profile_picture='example.com/profile_pic.jpg'
)


FAKE_REPORT = TeachersReport(
    teacher_id=1,
    teacher_name='pepa old',
    teacher_email='teacher@gmail.com',
    courses_users_reviews=[
        CourseViewForReport(
            course_id=7,
            title='Python',
            total_rating=9.5,
            sections_titles=['section1', 'section2'],
            users_reviews=[
                UsersReviewsViewForCourse(
                    user_id=5,
                    full_name='Peter Petroff',
                    email='peterthepete@gmail.com',
                    subscription='Active',
                    role='student',
                    completed=0.6,
                    rating=9.5,
                    review='amazing experience'
                )
            ]
        )
    ]
)


class ReportShould(unittest.TestCase):
    def test_reportReturnsCorrectly(self):
        fake_query_func = lambda x, y: [(
            7,
            'Python',
            0.95,
            'section1,section2',
            5,
            'Peter Petroff',
            'peterthepete@gmail.com',
            1,
            1,
            0.6,
            9.5,
            'amazing experience'
        )]
        expected = FAKE_REPORT

        result = report.get_teachers_report(FAKE_TEACHER, fake_query_func)

        self.assertEqual(result, expected)

    def test_reportReturnsNone_whenNoneFound(self):
        fake_query_func = lambda x, y: None
        expected = None

        result = report.get_teachers_report(FAKE_TEACHER, fake_query_func)

        self.assertEqual(result, expected)