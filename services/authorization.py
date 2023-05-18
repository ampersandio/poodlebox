from datetime import datetime, timedelta
from typing import Annotated
from functools import lru_cache

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import Settings
from data.models import User, TokenData
from services.users import get_user


PASSWORD_REQUIRED_LENGTH = 5
PASSWORD_SPECIAL_SYMBOLS = '!@#$%^&*()_+-=,./<>?"'

@lru_cache
def get_settings() -> Settings:
    return Settings()
settings = get_settings()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def hash_password(password: str):
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


def validate_password(password: str) -> None:
    if len(password) < PASSWORD_REQUIRED_LENGTH:
        raise HTTPException(status_code=400, detail='Password is too short, must be {PASSWORD_REQUIRED_LENGTH} symbols or more')
    
    # has_digit = False
    # has_symbol = False
    # for symbol in password:
    #     if symbol in PASSWORD_SPECIAL_SYMBOLS:
    #         has_symbol = True
    #     if symbol.isdigit():
    #         has_digit = True

    # if not has_digit:
    #     raise PasswordValidationError('Password needs to have at least one digit')

    # if not has_symbol:
    #     raise PasswordValidationError(f'Password needs to have at least one special symbol, allowed symbols are: {PASSWORD_SPECIAL_SYMBOLS}')
    

def validate_email(email: str) -> None:
    if '@' not in email or '.' not in email:
        raise HTTPException(status_code=400, detail='Email needs to contain "@" and "."')
    

def authenticate_user(email: str, password: str) -> User | None:
    user = get_user(email)

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=360)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(status_code=401, detail='Could not validate credentials')

    try: 
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email = payload.get('sub')
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = get_user(token_data.email)
    return user


