import unittest
from unittest.mock import patch
from api.services import admins
from api.data.models import User


MOCK_USER_1 = User(id=1, email='email@example.com', first_name='John', last_name='Doe', hashed_password='hashed_password', phone_number='1234567890', date_of_birth='2000-01-01', verified_email=True, approved=False,role='teacher',linked_in_profile='linkedin.com/in/johndoe',disabled=False,profile_picture=None)
MOCK_USER_2 = User(id=2,email='another_email@example.com',first_name='Jane',last_name='Smith',hashed_password='another_hashed_password',phone_number='9876543210',date_of_birth='1995-06-15',verified_email=True,approved=None,role='teacher',linked_in_profile='linkedin.com/in/janesmith',disabled=True,profile_picture='example.com/profile_picture')


class ServiceTestCase(unittest.TestCase):

    def test_student_status_disabled(self):
        student_id = 1
        disabled = True

        with patch("api.services.admins.update_query") as mock_update_query:
            admins.student_status(student_id, disabled)
            mock_update_query.assert_called_with("update users set disabled = 1 where id = ?;", (student_id,))


    def test_student_status_enabled(self):
        student_id = 1
        disabled = False

        with patch("api.services.admins.update_query") as mock_update_query:
            admins.student_status(student_id, disabled)
            mock_update_query.assert_called_with("update users set disabled = 0 where id = ?;", (student_id,))


    def test_course_status_disabled(self):
        course_id = 1
        disabled = True

        with patch("api.services.admins.update_query") as mock_update_query:
            admins.course_status(course_id, disabled)
            mock_update_query.assert_called_with("update courses set active = 1 where id = ?;", (course_id,))


    def test_course_status_enabled(self):
        course_id = 1
        disabled = False

        with patch("api.services.admins.update_query") as mock_update_query:
            admins.course_status(course_id, disabled)
            mock_update_query.assert_called_with("update courses set active = 0 where id = ?;", (course_id,))

    def test_remove_student(self):
        course_id = 1 
        student_id = 1

        with patch("api.services.admins.update_query") as mock_update_query:
            admins.remove_student(course_id, student_id)
            mock_update_query.assert_called_with("update users_has_courses set subscriptions_id = 3 where courses_id = ? and users_id = ?;", (course_id, student_id,))


    def test_with_pending_registrations(self):
        mock_data = [
            (1, 'email@example.com', 'John', 'Doe', 'hashed_password', '1234567890', '2000-01-01', True, False, 2, 'linkedin.com/in/johndoe', False, None),
            (2, 'another_email@example.com', 'Jane', 'Smith', 'another_hashed_password', '9876543210', '1995-06-15', True, None, 2, 'linkedin.com/in/janesmith', True, 'example.com/profile_picture'),
        ]

        with patch("api.services.admins.read_query") as mock_read_query:
            mock_read_query.return_value = mock_data

            registrations = admins.pending_registrations()

            assert len(registrations) == 2 
                    
            assert registrations[0] == MOCK_USER_1

            assert registrations[1] == MOCK_USER_2

            mock_read_query.assert_called_with("select * from users where role = 2 and approved = 0 and verified_email = 1;")


    def test_without_pending_registrations(self):
        mock_data = []

        with patch("api.services.admins.read_query") as mock_read_query:
            mock_read_query.return_value = mock_data

            registrations = admins.pending_registrations()

            assert len(registrations) == 0
                    
            mock_read_query.assert_called_with("select * from users where role = 2 and approved = 0 and verified_email = 1;")


    def test_judge_registration(self):
        with patch("api.services.admins.update_query") as mock_update_query:

            admins.judge_registration(1, True)

            mock_update_query.assert_called_with("update users set approved = 1 where id = ?;", (1,))

            admins.judge_registration(2, False)

            mock_update_query.assert_called_with("delete from users where approved = 0 and id = ?;", (2,))