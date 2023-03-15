from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
# from requests_oauthlib import OAuth2Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.certification as certification_crud
import api.models.user as user_model
import api.schemas.user as user_schema
import api.cruds.user as user_crud
import api.schemas.token as token_schema
from api.db import get_db

router = APIRouter()


# CLIENT_ID = 'b811937cf10d9b379129'
# CLIENT_SECRET = '3b461ccaf29125635461541f506e175a20f15d32'

# github = OAuth2Session(CLIENT_ID, redirect_uri='http://localhost:8000/callback/github')


ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@router.get('/items/')
async def read_items(token: str = Depends(oauth2_scheme)):
    return {'token': token}

# @router.get('/login/github')
# async def login_github():
#     pass

# @router.get('/login/github/callback')
# async def login_github_callback():
#     pass

# fake_users_db = {
#     'johndoe': {
#         'username': 'johndoe',
#         'full_name': 'John Doe',
#         'email': 'johndoe@example.com',
#         'hashed_password': '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
#         'disabled': False,
#     }
# }


# class User(BaseModel):
#     username: str
#     email: Union[str, None] = None
#     full_name: Union[str, None] = None
#     disabled: Union[bool, None] = None


# class UserInDB(User):
#     hashed_password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

router = APIRouter()


@router.post('/token', response_model=token_schema.Token)
async def login_for_access_token(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = certification_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = certification_crud.create_access_token(
        data={'sub': user.github_id}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/users/me/', response_model=user_schema.User)
async def read_users_me(current_user: user_model.User = Depends(certification_crud.get_current_active_user)):
    return user_crud.convert_usermodel_to_user(current_user)


@router.get('/users/me/items/')
async def read_own_items(current_user: user_model.User = Depends(certification_crud.get_current_active_user)):
    return [{'item_id': 'Foo', 'owner': current_user.github_id}]