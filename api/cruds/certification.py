
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.user as user_crud 
import api.models.user as user_model
import api.schemas.user as user_schema
import api.schemas.token as token_schema

from api.db import get_db

SECRET_KEY = 'b376cefceeb385ca0bf1a82623225cc520154a65d4cfb1b4f38eb70590e6ea8b'
ALGORITHM = 'HS256'

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(db: AsyncSession, github_id: str, password: str):
    user: user_schema.UserWithPassword = user_crud.convert_usermodel_to_user_with_password(user_crud.get_user_in_github_id(db, github_id))
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> Optional[user_model.User]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        github_id: str = payload.get('sub')
        if github_id is None:
            raise credentials_exception
        token_data = token_schema.TokenData(github_id=github_id)
    except JWTError:
        raise credentials_exception
    # user = user_crud.get_user(fake_users_db, username=token_data.github_id)
    user = user_crud.get_user_in_github_id(db=db, github_id=token_data.github_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Optional[user_model.User] = Depends(get_current_user)) -> user_model.User:
    if current_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    if current_user.disabled == 1:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user