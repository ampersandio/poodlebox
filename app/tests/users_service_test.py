from datetime import date

import unittest
from api.services import users
from api.data.models import User


FAKE_USER1 = User(
    id=1,
    email='fake_mail1@gmail.com',
    first_name='Peter',
    last_name='Petroff',
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


class UsersServiceShould(unittest.TestCase):
    def test_getUser_returnsCorrectly(self):
        fake_query_func = lambda x, y: [(
            FAKE_USER1.id, 
            FAKE_USER1.email, 
            FAKE_USER1.first_name, 
            FAKE_USER1.last_name,
            FAKE_USER1.hashed_password,
            FAKE_USER1.phone_number,
            FAKE_USER1.date_of_birth,
            FAKE_USER1.verified_email,
            FAKE_USER1.approved,
            2,
            FAKE_USER1.linked_in_profile,
            FAKE_USER1.disabled,
            FAKE_USER1.profile_picture
            )]
        expected = FAKE_USER1

        result = users.get_user(FAKE_USER1.email, fake_query_func)

        self.assertEqual(result, expected)

    def test_getUser_returnsNone_whenUserNotFound(self):
        fake_query_func = lambda x, y: None
        expected = None

        result = users.get_user('', fake_query_func)

        self.assertEqual(result, expected)

    def test_getUserByID_returnsCorrectly(self):
        fake_query_func = lambda x, y: [(
            FAKE_USER1.id, 
            FAKE_USER1.email, 
            FAKE_USER1.first_name, 
            FAKE_USER1.last_name,
            FAKE_USER1.hashed_password,
            FAKE_USER1.phone_number,
            FAKE_USER1.date_of_birth,
            FAKE_USER1.verified_email,
            FAKE_USER1.approved,
            FAKE_USER1.role,
            FAKE_USER1.linked_in_profile,
            FAKE_USER1.disabled,
            FAKE_USER1.profile_picture
            )]
        expected = FAKE_USER1

        result = users.get_user_by_id(FAKE_USER1.id)

        self.assertEqual(result, expected)

    def test_getUserByID_returnsNone_whenUserNotFound(self):
        fake_query_func = lambda x, y: None
        expected = None

        result = users.get_user_by_id(99, fake_query_func)

        self.assertEqual(result, expected)