import unittest
from api.data.models import CourseCreate, CourseShow, Course, CoursesShowStudent, TeacherShow
from api.services import courses


class CourseServiceShould(unittest.TestCase):
    def test_get_all_coursesAnonymoysWithData(self):
        db=lambda q:[(1,"Python","Comprehensive course on Python","OOP,DSA,Web",0,5.5,5.99,"Programming","pic.jpeg",1,"Sasho","Nedelev","0883837273726","anedelev@gmail.com","linkedin")]
        data=[(1,"Python","Comprehensive course on Python","OOP,DSA,Web",0,5.5,5.99,"Programming","pic.jpeg",1,"Sasho","Nedelev","0883837273726","anedelev@gmail.com","linkedin")]
        owner=TeacherShow.read_from_query_result(*data[0][9:])
        expected=[CourseShow.read_from_query_result(*data[0][:9],teacher=owner)]
        result=courses.get_courses_anonymous(db)
        self.assertEqual(expected,result)
    
    def test_get_all_coursesAnonymousNoData(self):
        db=lambda q:[]
        expected=[]
        result=courses.get_courses_anonymous(db)
        self.assertEqual(expected,result)
    
    def test_get_all_coursesTeacherWithData(self):
        db=lambda q:[(1,"Python","Comprehensive course on Python","OOP,DSA,Web",1,5.5,5.99,"Programming","pic.jpeg",1,"Sasho","Nedelev","0883837273726","anedelev@gmail.com","linkedin")]
        data=[(1,"Python","Comprehensive course on Python","OOP,DSA,Web",1,5.5,5.99,"Programming","pic.jpeg",1,"Sasho","Nedelev","0883837273726","anedelev@gmail.com","linkedin")]
        owner=TeacherShow.read_from_query_result(*data[0][9:])
        expected=[CourseShow.read_from_query_result(*data[0][:9],teacher=owner)]
        result=courses.get_courses_teacher(db)
        self.assertEqual(expected,result) 

    def test_get_all_coursesAnonymousNoData(self):
        db=lambda q:[]
        expected=[]
        result=courses.get_courses_teacher(db)
        self.assertEqual(expected,result)
    
    def test_get_all_coursesStudentWithData(self):
        db=lambda q,id:[(1,"Python","Comprehensive course on Python","OOP,DSA,Web",1,5.5,5.99,"Programming","pic.jpeg",1,"Sasho","Nedelev","0883837273726","anedelev@gmail.com","linkedin")]
        data=[(1,"Python","Comprehensive course on Python","OOP,DSA,Web",1,5.5,5.99,"Programming","pic.jpeg",1,"Sasho","Nedelev","0883837273726","anedelev@gmail.com","linkedin")]
        owner=TeacherShow.read_from_query_result(*data[0][9:])
        expected=[CourseShow.read_from_query_result(*data[0][:9],teacher=owner)]
        result=courses.get_courses_student(2,db)
        self.assertEqual(expected,result) 

    def test_get_all_coursesAnonymousNoData(self):
        db=lambda q,id:[]
        expected=[]
        result=courses.get_courses_student(2,db)
        self.assertEqual(expected,result)
    

    def test_get_course_byIdWithData(self):
        db=lambda q,id:[(1,"Python","Comprehensive course on Python","OOP,DSA,Web",1,5.5,5.99,"Programming","pic.jpeg",1,"Sasho","Nedelev","0883837273726","anedelev@gmail.com","linkedin")]
        data=[(1,"Python","Comprehensive course on Python","OOP,DSA,Web",1,5.5,5.99,"Programming","pic.jpeg",1,"Sasho","Nedelev","0883837273726","anedelev@gmail.com","linkedin")]
        owner=TeacherShow.read_from_query_result(*data[0][9:])
        expected=CourseShow.read_from_query_result(*data[0][:9],teacher=owner)
        result=courses.get_course_by_id(1,db)
        self.assertEqual(expected,result) 
    
    def test_get_course_byIdNoData(self):
        db=lambda q,id:[(None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)]
        expected=None
        result=courses.get_course_by_id(2,db)
        self.assertEqual(expected,result)
    
    def test_get_students_courses_withData(self):
        db=lambda q,id:[(1,"Python","Comprehensive course on Python","OOP,DSA,Web",1,5.5,5.99,"Programming",50,1,1,"Sasho","Nedelev","0883837273726","anedelev@gmail.com","linkedin")]
        data=[(1,"Python","Comprehensive course on Python","OOP,DSA,Web",1,5.5,5.99,"Programming",50,1,1,"Sasho","Nedelev","0883837273726","anedelev@gmail.com","linkedin")]
        owner=TeacherShow.read_from_query_result(*data[0][10:])
        expected=[CoursesShowStudent.read_from_query_result(*data[0][:10],teacher=owner)]
        result=courses.get_students_courses(2,db)
        self.assertEqual(expected,result) 
    
    def test_get_students_coursesNoData(self):
        db=lambda q,id:[]
        expected=[]
        result=courses.get_students_courses(2,db)
        self.assertEqual(expected,result)
    
    def test_get_students_coursesByIdWithData(self):
        db=lambda q,id:[(1,"Python","Comprehensive course on Python","OOP,DSA,Web",1,5.5,5.99,"Programming",50,1,1,"Sasho","Nedelev","0883837273726","anedelev@gmail.com","linkedin")]
        data=[(1,"Python","Comprehensive course on Python","OOP,DSA,Web",1,5.5,5.99,"Programming",50,1,1,"Sasho","Nedelev","0883837273726","anedelev@gmail.com","linkedin")]
        owner=TeacherShow.read_from_query_result(*data[0][10:])
        expected=CoursesShowStudent.read_from_query_result(*data[0][:10],teacher=owner)
        result=courses.get_student_course_by_id(2,1,db)
        self.assertEqual(expected,result) 

    def test_insertSection_returnsCorrectly(self):
        fake_query_func = lambda x, y: 5
        expected = 5

        result = courses.insert_section('', 10, fake_query_func)

        self.assertEqual(result, expected)
    
    def test_addCoursePhoto_returnsNone_whenCourseNotFound(self):
        fake_get_course_by_id_func = lambda x: None
        expected = None

        result = courses.add_course_photo('', 99, fake_get_course_by_id_func)

        self.assertEqual(result, expected)

    def test_insertContentType_returnsCorrectly(self):
        fake_query_func = lambda x, y: 5
        expected = 5

        result = courses.insert_content_type('', fake_query_func)

        self.assertEqual(result, expected)

    def test_deleteSection_returnsNone_whenSectionNotFound(self):
        fake_get_section_by_id_func = lambda x: None
        expected = None

        result = courses.delete_section(5, get_section_by_id_func=fake_get_section_by_id_func)

        self.assertEqual(result, expected)

    def test_approveEnrollment_returnsTrue(self):
        fake_query_func = lambda x, y: True
        expected = True

        result = courses.approve_enrollment(1, 2, fake_query_func)

        self.assertEqual(result, expected)

    def test_approveEnrollment_returnsFalse(self):
        fake_query_func = lambda x, y: False
        expected = False

        result = courses.approve_enrollment(1, 2, fake_query_func)

        self.assertEqual(result, expected)

    def test_rejectEnrollment_returnsTrue(self):
        fake_query_func = lambda x, y: True
        expected = True

        result = courses.reject_enrollment(1, 2, fake_query_func)

        self.assertEqual(result, expected)

    def test_rejectEnrollment_returnsFalse(self):
        fake_query_func = lambda x, y: False
        expected = False

        result = courses.reject_enrollment(1, 2, fake_query_func)

        self.assertEqual(result, expected)

    def test_checkOwnership_returnsTrue(self):
        fake_query_func = lambda x, y: [(1,)]
        expected = True

        result = courses.check_ownership(1, 2, fake_query_func)

        self.assertEqual(result, expected)
    
    def test_checkOwnership_returnsFalse(self):
        fake_query_func = lambda x, y: [(0,)]
        expected = False

        result = courses.check_ownership(1, 2, fake_query_func)

        self.assertEqual(result, expected)
    
    def test_getCourseOwner_returnsCorrectly(self):
        fake_query_func = lambda x, y: [(1,)]
        expected = 1

        result = courses.get_course_owner(7, fake_query_func)

        self.assertEqual(result, expected)

    def test_activateCourse_returnsTrue(self):
        fake_query_func = lambda x, y: True
        expected = True

        result = courses.activate_course(7, fake_query_func)

        self.assertEqual(result, expected)

    def test_activateCourse_returnsFalse(self):
        fake_query_func = lambda x, y: False
        expected = False

        result = courses.activate_course(7, fake_query_func)

        self.assertEqual(result, expected)

    def test_deactivateCourse_returnsTrue(self):
        fake_query_func = lambda x, y: True
        expected = True

        result = courses.deactivate_course(7, fake_query_func)

        self.assertEqual(result, expected)

    def test_deactivateCourse_returnsFalse(self):
        fake_query_func = lambda x, y: False
        expected = False

        result = courses.deactivate_course(7, fake_query_func)

        self.assertEqual(result, expected)