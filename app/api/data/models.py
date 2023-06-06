from pydantic import BaseModel, validator, EmailStr,  constr, conint
from datetime import date,datetime 

class StudentRegistration(BaseModel):
    email: EmailStr
    first_name: constr(min_length=1, max_length=20)
    last_name: constr(min_length=1, max_length=20)
    password: str
    date_of_birth: date

class TeacherRegistration(StudentRegistration):
    phone_number: str
    linked_in_profile: str

class TeacherShow(BaseModel):
    id: int
    first_name: constr(min_length=1, max_length=20)
    last_name: constr(min_length=1, max_length=20)
    email: EmailStr
    phone_number: str
    linked_in_profile: str

    @classmethod
    def read_from_query_result(cls, id:int, first_name:str, last_name:str, phone_number:str, email:EmailStr, linked_in_profile:str):
        return cls(id=id, first_name=first_name, last_name=last_name, phone_number=phone_number, email=email, linked_in_profile=linked_in_profile)

class User(BaseModel):
    id: int
    email: EmailStr
    first_name: constr(min_length=1, max_length=20)
    last_name: constr(min_length=1, max_length=20)
    hashed_password: str
    phone_number: str | None
    date_of_birth: date
    verified_email: bool
    approved: bool | None
    role: str
    linked_in_profile: str | None
    disabled: bool
    profile_picture: str | None

    @validator("role")
    def validate_role(cls, role):
        allowed_roles = ["student", "teacher", "admin"]
        if role not in allowed_roles:
            raise ValueError(f"Role must be one of {allowed_roles}")
        return role

    @classmethod
    def from_query(
        cls,
        id: int,
        email: EmailStr,
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
        profile_picture: str | None,
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
            profile_picture=profile_picture,
        )

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None

class ContentCreate(BaseModel):
    title: str
    description: str
    content_type: str
    link: str | None = None


class Content(ContentCreate):
    id: int

    @classmethod
    def read_from_query_result(cls, id:int, title:str, description:str, content_type:str, link:str):
        return cls(id=id, title=title, description=description, content_type=content_type, link=link)

    def __eq__(self, other: object) -> bool:
        return self.title == other.title

class SectionCreate(BaseModel):
    title: str
    content: list[ContentCreate] | None = None


class Section(SectionCreate):
    id: int

    @classmethod
    def read_from_query_result(cls, id: int, title: str, content: list[Content] | None = None):
        return cls(id=id, title=title, content=content or [])

    # def __eq__(self, other: object) -> bool:
    #     if isinstance(other, Section):
    #         return self.id == other.id
    #     return False

class BaseCourse(BaseModel):
    title: str
    description: str
    objectives: str
    premium: bool
    price: float | None = None
    course_picture: str | None = None


class CourseCreate(BaseCourse):
    tags: list[str]


class Course(BaseCourse):
    id: int
    active: bool
    owner: int

    @classmethod
    def read_from_query_result(cls, id:int, title:str, description:str, objectives:str, premium:bool, active:bool, owner:int, price:float, course_picture:str):
        return cls(
            id=id,
            title=title,
            description=description,
            objectives=objectives,
            premium=premium,
            active=active,
            owner=owner,
            price=price,
            course_picture=course_picture,
        )

class CourseShow(BaseCourse):
    id: int
    rating: float | None = None
    tags: list[str]
    teacher: TeacherShow | None = None

    @classmethod
    def read_from_query_result(cls,id:int, title:str, description:str, objectives:str, premium:bool, rating:float, price:float, tags:list[str], course_picture:str, teacher: TeacherShow):

        if tags is not None:
            tags = [x for x in tags.split(",")]

        # premium = bool(premium)

        return cls(
            id=id,
            title=title,
            description=description,
            objectives=objectives,
            premium=premium,
            rating=rating,
            price=price,
            tags=tags,
            course_picture=course_picture,
            teacher=teacher,
        )

# class CourseShowId(CourseShow):
#     sections: list[Section] | None = None

#     @classmethod
#     def read_from_query_result(cls, id:int, title:str, description:str, objectives:str, premium:bool, rating:float, price:float, tags:list[str], course_picture:str, teacher:TeacherShow, sections:list[Section]):

#         if tags is not None:
#             tags = [x for x in tags.split(",")]

#         # premium = bool(premium)
#         return cls(
#             id=id,
#             title=title,
#             description=description,
#             objectives=objectives,
#             premium=premium,
#             rating=rating,
#             price=price,
#             tags=tags,
#             course_picture=course_picture,
#             teacher=teacher,
#             sections=sections,
#         )

class CoursesShowStudent(BaseModel):
    id: int
    title: str
    description: str
    objectives: str
    premium: bool
    rating: float | None = None
    price: float | None = None
    tags: list[str]
    progress: int
    subscription_status: str
    teacher: TeacherShow | None = None

    @classmethod
    def read_from_query_result(cls,id:int, title:str, description:str, objectives:str, premium:bool, rating:float, price:float, tags:list[str], progress:int, subscription_status:str, teacher:TeacherShow):

        if tags is not None:
            tags = [x for x in tags.split(",")]

        # premium = bool(premium)

        return cls(
            id=id,
            title=title,
            description=description,
            objectives=objectives,
            premium=premium,
            rating=rating,
            price=price,
            tags=tags,
            progress=progress,
            subscription_status=subscription_from_id((subscription_status)),
            teacher=teacher,
        )

class CourseUserReview(BaseModel):
    course_id: int
    title: str
    total_rating: float | None
    sections_titles: list[str] | None
    user_id: int
    full_name: str
    email: EmailStr
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
        email: EmailStr,
        subscription_id: int,
        role_id: int,
        completed_sections: float,
        rating: float | None,
        review: str | None,
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
            review=review,
        )

class UsersReviewsViewForCourse(BaseModel):
    user_id: int
    full_name: str
    email: EmailStr
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
            review=course_user_review.review,
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
    teacher_email: str
    courses_users_reviews: list[CourseViewForReport]


class TeacherProfile(BaseModel):
    email: EmailStr
    first_name: constr(min_length=1, max_length=20)
    last_name: constr(min_length=1, max_length=20)
    phone_number: str | None
    date_of_birth: date
    verified_email: bool
    approved: bool | None
    role: str
    linked_in_profile: str | None
    profile_picture: str | None

    @classmethod
    def from_user(cls, user: User):
        return cls(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            date_of_birth=user.date_of_birth,
            verified_email=user.verified_email,
            approved=user.approved,
            role=user.role,
            linked_in_profile=user.linked_in_profile,
            profile_picture=user.profile_picture
        )


class EditTeacherProfile(BaseModel):
    new_password: str | None
    new_password_again: str | None
    phone_number: str | None
    linked_in_profile: str | None
    profile_picture: str | None

    @classmethod
    def from_user(cls, user: User):
        return cls(
            phone_number=user.phone_number,
            linked_in_profile=user.linked_in_profile,
            profile_picture=user.profile_picture
        )


class Review(BaseModel):
    id: int | None
    users_id: int
    courses_id: int
    rating: float
    description: str


class Subscription(BaseModel):
    enroll: bool

class SubscriptionStatus(BaseModel):
    subscription:str
    user_id:int
    course_id:int

    @classmethod
    def from_query(cls,subscription:str,user_id:int,course_id:int):
        return cls(subscription=subscription_from_id(subscription),user_id=user_id,course_id=course_id)

class Student(BaseModel):
    id: int
    first_name: constr(min_length=1, max_length=20)
    last_name: constr(min_length=1, max_length=20)
    email: EmailStr
    verified_email: bool
    date_of_birth: date
    total_number_of_courses: int
    number_of_pending_subscriptions: int
    number_of_active_subscriptions: int
    number_of_expired_subscriptions: int

    @classmethod
    def read_from_query_result(
        cls,
        id,
        first_name,
        last_name,
        email,
        verified_email,
        date_of_birth,
        total_number_of_courses,
        number_of_pending_subscriptions,
        number_of_active_subscriptions,
        number_of_expired_subscriptions,
    ):
        verified_email = bool(verified_email)
        return cls(
            id=id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            verified_email=verified_email,
            date_of_birth=date_of_birth,
            total_number_of_courses=total_number_of_courses,
            number_of_pending_subscriptions=number_of_pending_subscriptions,
            number_of_active_subscriptions=number_of_active_subscriptions,
            number_of_expired_subscriptions=number_of_expired_subscriptions,
        )
    

class PendingEnrollment(BaseModel):
    user_id: int
    course_id: int

    @classmethod
    def from_query(
        cls,
        user_id: int,
        course_id: int
    ):
        return cls(
            user_id=user_id,
            course_id=course_id
        )


class StudentEdit(BaseModel):
    new_password: str
    confirm_new_password: str

def subscription_from_id(id: int):
    subscription_from_subscription_id = {1: "Active", 2: "Pending", 3: "Expired"}
    return subscription_from_subscription_id[id]

def role_from_id(role_id: int) -> str:
    role_ids_to_roles = {1: "student", 2: "teacher", 3: "admin"}
    return role_ids_to_roles[role_id]

class Certificate(BaseModel):
    id: str
    user_id:int
    course_id: int
    issued_date: date

    @classmethod
    def read_from_query_result(cls, id,user_id,course_id, issued_date):
        return cls(id=id,user_id=user_id,course_id=course_id, issued_date=issued_date)

class Event(BaseModel):
    id:int|None=None
    name:str
    start:datetime
    end:datetime
    link_to_event:str

    @classmethod
    def read_from_query_result(cls,id,name,start,end,link_to_event):
        return cls(id=id,name=name,start=start,end=end,link_to_event=link_to_event)

class EventChange(BaseModel):
    name:str|None=None
    start:datetime|None=None
    end:datetime|None=None
    link_to_event:str|None=None

class EventCreate(BaseModel):
    name:str
    start:datetime
    end:datetime
    link_to_event:str
    @classmethod
    def read_from_query_result(cls,name,start,end,link_to_event):
        return cls(name=name,start=start,end=end,link_to_event=link_to_event)

class Calendar(BaseModel):
    id:int|None=None
    name:str
    course_id:int
    owner_id:int

    @classmethod
    def read_from_query_result(cls,id,name,course_id,owner_id):
        return cls(id=id,name=name,course_id=course_id,owner_id=owner_id)
    
class CalendarCreate(BaseModel):
    name:str
    course_id:int

    @classmethod
    def read_from_query_result(cls,name,course_id):
        return cls(name=name,course_id=course_id)

class CalendarById(BaseModel):
    id:int
    name:str
    course_id:int
    owner:TeacherShow
    events:list[Event]|None=None

    @classmethod
    def read_from_query_result(cls,id,name,course_id,owner,events):
        return cls(id=id,name=name,course_id=course_id,owner=owner,events=events)


class CalendarChange(BaseModel):
    owner_id:int


