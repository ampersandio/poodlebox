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
    verified_email: bool
    approved: bool | None
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
        phone_number: str | None,
        date_of_birth: date,
        verified_email: bool,
        approved: bool | None,
        role: int,
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

