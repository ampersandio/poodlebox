import api.utils.constants as constants

from typing import Annotated
from config import settings
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from api.data.models import StudentRegistration, TeacherRegistration, Token, User
import api.services.authorization as authorization_services
import api.services.users as user_services
from api.utils.utils import user_registration_mail, teacher_registration_mail

from jose import jwt

authorization_router = APIRouter(prefix='/authorization')


@authorization_router.post('/registration/students', tags=['Authentication'])
def register_student(request:Request, information: StudentRegistration) -> JSONResponse:
    host = "http://" + request.headers["host"]

    if user_services.get_user(information.email) is not None:
        raise HTTPException(status_code=400, detail=f'{constants.EMAIL_EXISTS} {information.email}')

    if not information.first_name:
        raise  HTTPException(status_code=400, detail=constants.FIRST_NAME_EMPTY)

    if not information.last_name:
        raise  HTTPException(status_code=400, detail=constants.LAST_NAME_EMPTY)
    
    if not information.date_of_birth:
        raise HTTPException(status_code=400, detail=constants.DATE_OF_BIRTH_EMPTY)

    authorization_services.validate_email(information.email)
    authorization_services.validate_password(information.password)

    information.password = authorization_services.hash_password(information.password)

    user_services.register_student(information)
    user_registration_mail(information,host)

    return JSONResponse(status_code=201, content={'msg': constants.STUDENT_REGISTRATION_SUCCESS})


@authorization_router.post('/registration/teachers', tags=['Authentication'])
def register_teacher(request:Request, information: TeacherRegistration, current_user: Annotated[User, Depends(authorization_services.get_current_user)]) -> JSONResponse:
    host = "http://" + request.headers["host"]
    if current_user.role != constants.ADMIN_ROLE:
        raise HTTPException(status_code=400, detail=constants.ONLY_ADMIN_TEACHER)

    if user_services.get_user(information.email) is not None:
        raise HTTPException(status_code=400, detail=f'{constants.EMAIL_EXISTS} {information.email}')

    if not information.first_name:
        raise  HTTPException(status_code=400, detail=constants.FIRST_NAME_EMPTY)

    if not information.last_name:
        raise  HTTPException(status_code=400, detail=constants.LAST_NAME_EMPTY)
    
    if not information.date_of_birth:
        raise HTTPException(status_code=400, detail=constants.DATE_OF_BIRTH_EMPTY)
    
    if not information.phone_number:
        raise HTTPException(status_code=400, detail=constants.PHONE_EMPTY)
    
    if not information.linked_in_profile:
        raise HTTPException(status_code=400, detail=constants.LINKED_IN_PROFILE)

    authorization_services.validate_email(information.email)

    authorization_services.validate_password(information.password)

    information.password = authorization_services.hash_password(information.password)

    user_services.register_teacher(information)

    user_registration_mail(information,host)
    teacher_registration_mail(information)


    return JSONResponse(status_code=201, content={'msg': constants.TEACHER_REGISTRATION_SUCCESS})


@authorization_router.post('/login', tags=['Authentication'])
def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:

    user = authorization_services.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail=constants.WRONG_AUTHENTICATION)
    
    access_token_expires = timedelta(minutes=settings.access_token_expires_minutes)
    access_token = authorization_services.create_access_token({'sub': user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}



@authorization_router.get('/token/{token}', tags=['Authentication'])
def get_user(token:str):
    '''
    Endpoint to validate mail account.
    
    '''

    user = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    user = user_services.get_user(user["sub"])

    if user is not None:
        authorization_services.verify_mail(user)
        return JSONResponse(status_code=201, content={'msg': constants.EMAIL_VALIDATION_SUCCEESS})
    else:
        raise HTTPException(status_code=401, detail=constants.EMAIL_VALIDATION_FAIL)