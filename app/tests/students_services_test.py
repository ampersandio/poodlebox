import unittest
from unittest.mock import Mock, patch
from api.services import students
from api.data.models import Student, Subscription
from api.services.authorization import hash_password


class StudentsServiceShould(unittest.TestCase):
   def test_students_courses_idsWithValidData(self):
    db=lambda q,id:[("1,2,3",)]
    expected=[1,2,3]
    result=students.get_students_courses_id(1,db)
    self.assertEqual(expected,result)
   
   def test_students_courses_idsNoData(self):
    db=lambda q,id:[(None,)]
    expected=[]
    result=students.get_students_courses_id(1,db)
    self.assertEqual(expected,result)
   
   def test_students_active_coursesWithData(self):
    db=lambda q,id:[("1,2,3",)]
    expected=[1,2,3]
    result=students.get_students_active_courses(1,db)
    self.assertEqual(expected,result)

   def test_students_active_coursesNoData(self):
    db=lambda q,id:[(None,)]
    expected=[]
    result=students.get_students_active_courses(1,db)
    self.assertEqual(expected,result)

   def test_check_enrollmentstatus_validData(self):
    db=lambda q,id:[(3,)]
    expected=3
    result=students.check_enrollment_status(1,1,db)
    self.assertEqual(expected,result)
   
   def test_check_enrollmentStatusNodata(self):
    db=lambda q,id:[]
    expected=None
    result=students.check_enrollment_status(1,1,db)
    self.assertEqual(expected,result)
   
   def test_get_students_premiumCourses(self):
    db=lambda q,id:[(1,)]
    expected=1
    result=students.get_students_number_courses_premium(1,db)
    self.assertEqual(expected,result)

   def test_enroll_in_courseEnrollTrueExpiredFalse(self):
    db=lambda q,id:1
    subscription=Subscription(enroll=True)
    result=students.enroll_in_course(1,2,subscription,False,db)
    expected=None
    self.assertEqual(expected,result)
   
   def test_enroll_inCourseEnrollTrueExpiredTrue(self):
    db=lambda q,id:None
    subscription=Subscription(enroll=True)
    result=students.enroll_in_course(1,2,subscription,True,db)
    expected=None
    self.assertEqual(expected,result)
   
   def test_enrollInCourseEnrollFalse(self):
    db=lambda q,id:None
    subscription=Subscription(enroll=False)
    result=students.enroll_in_course(1,2,subscription,False,db)
    expected=None
    self.assertEqual(expected,result)


   def test_get_profile(self):
    db=lambda q,id:[(1,"Blago","Aleksandrova","blago@abv.bg",True,"1993-06-11",3,1,1,1)]
    data=[(1,"Blago","Aleksandrova","blago@abv.bg",True,"1993-06-11",3,1,1,1)]
    result=students.get_profile(1,db)
    expected=Student.read_from_query_result(*data[0])
    self.assertEqual(expected,result)
   
   def test_update_password(self):
    db=lambda q,id:None
    expected=None
    result=students.change_password(1,"NewPassword123",db)
    self.assertEqual(expected,result)


    
    