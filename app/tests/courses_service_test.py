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
    

 