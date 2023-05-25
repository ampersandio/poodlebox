from pydantic import BaseModel
from datetime import date
from collections import defaultdict


class User(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    phone_number: str | None
    date_of_birth: date
    verified_email: bool
    approved: bool | None
    role: str
    linked_in_profile: str | None
    disabled: bool
    profile_picture: str | None

    @classmethod
    def from_query(
        cls,
        id: int,
        email: str,
        first_name: str,
        last_name: str,
        hashed_password: str,
        phone_number: str | None,
        date_of_birth: date,
        verified_email: bool,
        approved: bool | None,
        role_id: int,
        linked_in_profile: str | None,
        disabled: bool,
        profile_picture: str | None
    ):
        
        return cls(
            id=id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            hashed_password=hashed_password,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            verified_email=verified_email,
            approved=approved,
            role=role_from_id(role_id),
            linked_in_profile=linked_in_profile,
            disabled=disabled,
            profile_picture=profile_picture
        )
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserInDB(BaseModel):
    hashed_password: str


class StudentRegistration(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str
    date_of_birth: date


class TeacherRegistration(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str
    date_of_birth: date
    phone_number: str
    linked_in_profile: str

class Content(BaseModel):
    id:int
    title:str
    description:str
    content_type:str

    @classmethod
    def read_from_query_result(cls,id,title,description,content_type):
        return cls(id=id,title=title,description=description,content_type=content_type)

class ContentCreate(BaseModel):
    title:str
    description:str
    content_type:str

class Section(BaseModel):
    id: int
    title: str
    content: list[Content] | None = None
    
    @classmethod
    def read_from_query_result(cls, id: int, title: str, content: list[Content] | None = None):
        return cls(id=id, title=title, content=content or [])  
    
class SectionCreate(BaseModel):
    title: str
    content: list[ContentCreate] | None = None
    
class TeacherShow(BaseModel):
    id:int
    first_name:str
    last_name:str
    phone_number:str
    email:str
    linked_in_profile:str
    
    @classmethod
    def read_from_query_result(cls,id,first_name,last_name,phone_number,email,linked_in_profile):
        return cls(id=id,first_name=first_name,last_name=last_name,phone_number=phone_number,email=email,linked_in_profile=linked_in_profile)
    
class Course(BaseModel):
    id:int
    title:str
    description:str
    objectives:str
    premium:bool
    active:bool
    owner:int
    price:float | None = None
    course_picture:str | None = None
    
    @classmethod
    def read_from_query_result(cls,id,title,description,objectives,premium,active,owner,price,course_picture):
        return cls(id=id,title=title,description=description,objectives=objectives,premium=premium,active=active,owner=owner,price=price,course_picture=course_picture)


class CourseShow(BaseModel):
    id:int
    title:str
    description:str
    objectives:str
    premium:bool
    rating:float|None=None
    price:float|None=None
    tags:list[str]
    teacher:TeacherShow|None=None
    
    @classmethod
    def read_from_query_result(cls,id,title,description,objectives,premium,rating,price,tags,teacher):
        if tags is not None:
            tags=[x for x in tags.split(",")]
        premium=bool(premium)
        return cls(id=id,title=title,description=description,objectives=objectives,premium=premium,rating=rating,price=price,tags=tags,teacher=teacher)

class CourseShowId(BaseModel):
    id:int
    title:str
    description:str
    objectives:str
    premium:bool
    rating:float|None=None
    price:float|None=None
    tags:list[str]
    teacher:TeacherShow|None=None
    sections:list[Section]|None=None
    
    @classmethod
    def read_from_query_result(cls,id,title,description,objectives,premium,rating,price,tags,teacher,sections):
        if tags is not None:
            tags=[x for x in tags.split(",")]
        premium=bool(premium)
        return cls(id=id,title=title,description=description,objectives=objectives,premium=premium,rating=rating,price=price,tags=tags,teacher=teacher,sections=sections)

class CoursesShowStudent(BaseModel):
    id:int
    title:str
    description:str
    objectives:str
    premium:bool
    rating:float|None=None
    price:float|None=None
    tags:list[str]
    progress:int
    subscripton_status:str
    teacher:TeacherShow|None=None
    sections:list[Section]|None=None
    
    @classmethod
    def read_from_query_result(cls,id,title,description,objectives,premium,rating,price,tags,progress,subscripton_status,teacher,sections):
        if subscripton_status==2:
            subscripton_status="Pending"
        elif subscripton_status==1:
            subscripton_status="Active"
        elif subscripton_status==3:
            subscripton_status="Expired"
        if tags is not None:
            tags=[x for x in tags.split(",")]
        premium=bool(premium)
        return cls(id=id,title=title,description=description,objectives=objectives,premium=premium,rating=rating,price=price,tags=tags,progress=progress,subscripton_status=subscripton_status,teacher=teacher,sections=sections)
    

class CourseUserReview(BaseModel):
    course_id: int
    title: str
    total_rating: float | None
    sections_titles: list[str] | None
    user_id: int
    full_name: str
    email: str
    subscription: str
    role: str
    completed_sections: float
    rating: float | None
    review: str | None

    @classmethod
    def from_query(
        cls,
        course_id: int,
        title: str,
        total_rating: float | None,
        sections_titles: str | None,
        user_id: int,
        full_name: str,
        email: str,
        subscription_id: int,
        role_id: int,
        completed_sections: float,
        rating: float | None,
        review: str | None
    ):
        return cls(
            course_id=course_id,
            title=title,
            total_rating=round(total_rating*10, 1),
            sections_titles=sections_titles.split(','),
            user_id=user_id,
            full_name=full_name,
            email=email,
            subscription=subscription_from_id(subscription_id),
            role=role_from_id(role_id),
            completed_sections=completed_sections,
            rating=rating,
            review=review
        )
    

class UsersReviewsViewForCourse(BaseModel):
    user_id: int
    full_name: str
    email: str
    subscription: str
    role: str
    completed: float
    rating: float | None
    review: str | None

    @classmethod
    def from_CourseUserReview(cls, course_user_review: CourseUserReview):
        return cls(
            user_id=course_user_review.user_id,
            full_name=course_user_review.full_name,
            email=course_user_review.email,
            subscription=course_user_review.subscription,
            role=course_user_review.role,
            completed=course_user_review.completed_sections,
            rating=course_user_review.rating,
            review=course_user_review.review
        )


class CourseViewForReport(BaseModel):
    course_id: int
    title: str
    total_rating: float | None
    sections_titles: list[str] | None
    users_reviews: list[UsersReviewsViewForCourse]


class TeachersReport(BaseModel):
    teacher_id: int
    teacher_name: str
    courses_users_reviews: list[CourseViewForReport]

    
class Subscription(BaseModel):
    enroll:bool

class CourseCreate(BaseModel):
    title:str
    description:str
    objectives:str
    premium:bool
    price:float|None=None
    tags:list[str]
    course_pic:str|None=None


class Student(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:str
    verified_email:bool
    date_of_birth:date
    total_number_of_courses:int
    number_of_pending_subscriptions:int
    number_of_active_subscriptions:int
    number_of_expired_subscriptions:int
    
    @classmethod
    def read_from_query_result(cls,id,first_name,last_name,email,verified_email,date_of_birth,total_number_of_courses,number_of_pending_subscriptions,number_of_active_subscriptions,number_of_expired_subscriptions):
        verified_email=bool(verified_email)
        return cls(id=id,first_name=first_name,last_name=last_name,email=email,verified_email=verified_email,date_of_birth=date_of_birth,total_number_of_courses=total_number_of_courses,number_of_pending_subscriptions=number_of_pending_subscriptions,number_of_active_subscriptions=number_of_active_subscriptions,number_of_expired_subscriptions=number_of_expired_subscriptions)


class StudentEdit(BaseModel):
    new_password:str
    confirm_new_password:str


def subscription_from_id(id: int):
        subscription_from_subscription_id = {
                1: 'Active',
                2: 'Pending',
                3: 'Expired'
        }
        return subscription_from_subscription_id[id]


def role_from_id(role_id: int) -> str:
        role_ids_to_roles = {
                1: 'student',
                2: 'teacher',
                3: 'admin'
        }
        return role_ids_to_roles[role_id]