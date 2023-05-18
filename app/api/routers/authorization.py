from typing import Annotated
from functools import lru_cache
from config import Settings
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from api.data.models import StudentRegistration, TeacherRegistration
import api.services.authorization as authorization_services
import api.services.users as user_services


authorization_router = APIRouter(prefix='/authorization')

@lru_cache
def get_settings() -> Settings:
    return Settings()
settings = get_settings()


@authorization_router.post('/registration/students', tags=['Authentication'])
def register_student(information: StudentRegistration) -> JSONResponse:
    if user_services.get_user(information.email) is not None:
        raise HTTPException(status_code=400, detail=f'There already is a registered user with email: {information.email}')

    if not information.first_name:
        raise  HTTPException(status_code=400, detail='First name cannot be empty')

    if not information.last_name:
        raise  HTTPException(status_code=400, detail='Last name cannot be empty')
    
    if not information.date_of_birth:
        raise HTTPException(status_code=400, detail='Date of birth cannot be empty')

    authorization_services.validate_email(information.email)

    authorization_services.validate_password(information.password)

    information.password = authorization_services.hash_password(information.password)
    #information.date_of_birth = date.fromisoformat(information.date_of_birth)

    user_services.register_student(information)

    return JSONResponse(status_code=201, content={'msg': 'Student registered successfully'})


@authorization_router.post('registration/teachers', tags=['Authentication'])
def register_teacher(information: TeacherRegistration) -> JSONResponse:
    if user_services.get_user(information.email) is not None:
        raise HTTPException(status_code=400, detail=f'There already is a registered user with email: {information.email}')

    if not information.first_name:
        raise  HTTPException(status_code=400, detail='First name cannot be empty')

    if not information.last_name:
        raise  HTTPException(status_code=400, detail='Last name cannot be empty')
    
    if not information.date_of_birth:
        raise HTTPException(status_code=400, detail='Date of birth cannot be empty')
    
    if not information.phone_number:
        raise HTTPException(status_code=400, detail='Phone number cannot be empty')
    
    if not information.linked_in_profile:
        raise HTTPException(status_code=400, detail='Linked in profile cannot be empty')

    authorization_services.validate_email(information.email)

    authorization_services.validate_password(information.password)

    information.password = authorization_services.hash_password(information.password)

    user_services.register_teacher(information)

    return JSONResponse(status_code=201, content={'msg': 'Student registered successfully'})


@authorization_router.post('/login', tags=['Authentication'])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:
    user = authorization_services.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail='Wrong username or password')
    
    access_token_expires = timedelta(minutes=settings.access_token_expires_minutes)
    access_token = authorization_services.create_access_token({'sub': user.email}, expires_delta=access_token_expires)

    return {'msg': 'Successfully logged in',
            'token': access_token,
            'token_type': 'bearer'
    }
