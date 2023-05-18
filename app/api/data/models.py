from pydantic import BaseModel
from datetime import date


class User(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    phone_number: str | None
    date_of_birth: date
    verified: bool
    role: int
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
        phone_number: str,
        date_of_birth: date,
        verified: bool,
        role: int,
        linked_in_profile: str,
        disabled: bool,
        profile_picture: str
    ):
        
        return cls(
            id=id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            hashed_password=hashed_password,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            verified=verified,
            role=role,
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
        if content_type==1:
            content_type='video'
        return cls(id=id,title=title,description=description,content_type=content_type)

class Section(BaseModel):
    id:int
    title:str
    content:list[Content]|None=None
    
    @classmethod
    def read_from_query_result(cls,id,title,content):
        return cls(id=id,title=title,content=content)

class TeacherShow(BaseModel):
    id:int
    first_name:str
    last_name:str
    phone_number:str
    linked_in_profile:str
    
    @classmethod
    def read_from_query_result(cls,id,first_name,last_name,phone_number,linked_in_profile):
        return cls(id=id,first_name=first_name,last_name=last_name,phone_number=phone_number,linked_in_profile=linked_in_profile)

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
    teacher:TeacherShow|None=None
    sections:list[Section]|None=None
    progress:int
    
    @classmethod
    def read_from_query_result(cls,id,title,description,objectives,premium,rating,price,tags,teacher,sections,progress):
        if tags is not None:
            tags=[x for x in tags.split(",")]
        premium=bool(premium)
        return cls(id=id,title=title,description=description,objectives=objectives,premium=premium,rating=rating,price=price,tags=tags,teacher=teacher,sections=sections,progress=progress)
    