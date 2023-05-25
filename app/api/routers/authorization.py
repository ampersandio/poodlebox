from typing import Annotated
from config import settings
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from api.data.models import StudentRegistration, TeacherRegistration, Token, User
import api.services.authorization as authorization_services
import api.services.users as user_services
from api.utils.utils import generate_html 
from mailjet_rest import Client

from jose import jwt

authorization_router = APIRouter(prefix='/authorization')

mailjet = Client(auth=(settings.api_key, settings.api_secret), version='v3.1')

@authorization_router.post('/registration/students', tags=['Authentication'])
def register_student(request:Request, information: StudentRegistration) -> JSONResponse:
    host = "http://" + request.headers["host"]

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

    user_services.register_student(information)

    data = generate_html(information.email,host)
    result = mailjet.send.create(data=data)

    print (result.status_code)
    print (result.json())

    return JSONResponse(status_code=201, content={'msg': 'Student registered successfully'})


@authorization_router.post('/registration/teachers', tags=['Authentication'])
def register_teacher(information: TeacherRegistration, current_user: Annotated[User, Depends(authorization_services.get_current_user)]) -> JSONResponse:
    if current_user.role != "admin":
        raise HTTPException(status_code=400, detail='Only an admin can register a teacher')

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

    return JSONResponse(status_code=201, content={'msg': 'Teacher registered successfully'})


@authorization_router.post('/login', tags=['Authentication'])
def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:
    user = authorization_services.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail='Wrong username or password')
    
    access_token_expires = timedelta(minutes=settings.access_token_expires_minutes)
    access_token = authorization_services.create_access_token({'sub': user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@authorization_router.get('/token/{token}', tags=['Authentication'])
def get_user(token:str):
    user = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    user = user_services.get_user(user["sub"])

    if user is not None:
        authorization_services.verify_mail(user)
        return JSONResponse(status_code=201, content={'msg': 'email validation successfull'})
    else:
        raise HTTPException(status_code=401, detail="Could not validate mail")