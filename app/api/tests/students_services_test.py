import unittest
from unittest.mock import Mock
from api.services import students
from api.data.models import Student

mock_db=Mock()
students.database=mock_db


class StudentsServiceShould(unittest.TestCase):
   def test_students_courses_idsWithValidData(self):
    mock_db.read_query.return_value=[(1,2,3)]
    expected=[1,2,3]
    result=students.get_students_courses_id(1)
    self.assertEqual(expected,result)
   
   def test_students_courses_idsNoData(self):
    mock_db.read_query.return_value=[(None,)]
    expected=[]
    result=students.get_students_courses_id(1)
    self.assertEqual(expected,result)
   
   def test_students_active_coursesWithData(self):
    mock_db.read_query.return_value=[(1,2,3)]
    expected=[1,2,3]
    result=students.get_students_active_courses(1)
    self.assertEqual(expected,result)

   def test_students_active_coursesNoData(self):
    mock_db.read_query.return_value=[(None,)]
    expected=[]
    result=students.get_students_active_courses(1)
    self.assertEqual(expected,result)
   
   def test_check_enrollmentstatus_validData(self):
    mock_db.read_query.return_value=[(3,)]
    expected=3
    result=students.check_enrollment_status(1)
    self.assertEqual(expected,result)
   
   def test_check_enrollmentStatusNodata(self):
    mock_db.read_query.return_value=[]
    expected=None
    result=students.check_enrollment_status(1)
    self.assertEqual(expected,result)
   
   def test_get_students_premiumCourses(self):
    mock_db.read_query.return_value=[(1,)]
    expected=1
    result=students.check_enrollment_status(1)
    self.assertEqual(expected,result)

   def test_enroll_in_courseEnrollTrueExpiredFalse(self):
    mock_db.insert_query.return_value=1
    result=students.enroll_in_course(1,2,True,False)
    expected=None
    self.assertEqual(expected,result)
   
   def test_enroll_inCourseEnrollTrueExpiredTrue(self):
    mock_db.update_query.return_value=None
    result=students.enroll_in_course(1,2,True,True)
    expected=None
    self.assertEqual(expected,result)
   
   def test_enrollInCourseEnrollFalse(self):
    mock_db.update_query.return_value=None
    result=students.enroll_in_course(1,2,False,False)
    expected=None
    self.assertEqual(expected,result)


   def test_get_profile(self):
    mock_db.read_query.return_value=[(1,"Blago","Aleksandrova","blago@abv.bg",True,"1993-06-11",3,1,1,1)]
    result=students.get_profile(1)
    expected=Student(id=1,first_name="Blago",last_name="Aleksandrova",email="blago@abv.bg",verified_email=True,date_of_birth="1993-06-11",total_number_of_courses=3,number_of_pending_subscriptions=1,number_of_active_subscriptions=1,number_of_expired_subscriptions=1)
    self.assertEqual(expected,result)
   
   def test_update_password(self):
    mock_db.update_query.reaturn_value=None
    expected=None
    result=students.change_password(1,"HIHI")
    self.assertEqual(expected,result)


    
    