from pydantic import BaseModel

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


    