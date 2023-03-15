from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from typing import Optional
# from requests_oauthlib import OAuth2Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer
from sqlalchemy.ext.asyncio import AsyncSession
from requests_oauthlib import OAuth2Session
from starlette.responses import RedirectResponse

import api.cruds.certification as certification_crud
import api.models.user as user_model
import api.schemas.user as user_schema
import api.cruds.user as user_crud
import api.schemas.token as token_schema
from api.db import get_db

router = APIRouter()


CLIENT_ID = 'b811937cf10d9b379129'
CLIENT_SECRET = '3b461ccaf29125635461541f506e175a20f15d32'
AUTHORIZATION_BASE_URL = 'https://github.com/login/oauth/authorize'
TOKEN_URL = 'https://github.com/login/oauth/access_token'
REDIRECT_URL = 'http://localhost:8000/login/github/callback'
# github = OAuth2Session(CLIENT_ID, redirect_uri='http://localhost:8000/callback/github')
session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URL)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
oauth2_scheme_end_point = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTHORIZATION_BASE_URL,
    tokenUrl=TOKEN_URL,
    scopes={'read': 'Read acceess', 'write': 'Write access'}
)

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

# 認証リダイレクト用エンドポイント
@router.get("/login/github")
async def login(request: Request):
    # GitHub OAuth認証の開始
    authorization_url, state = session.authorization_url(AUTHORIZATION_BASE_URL)

    # 認証用URLにリダイレクト
    return RedirectResponse(authorization_url)

# 認証後のコールバックURL
@router.get("/login/github/callback")
async def login_callback(code: str, state: str = None):
    # アクセストークンを取得するためのリクエストを送信
    session.fetch_token(
        token_url=TOKEN_URL,
        authorization_response=REDIRECT_URL + f"?code={code}",
        client_secret=CLIENT_SECRET
    )

    # ユーザー情報を取得
    user = session.get("https://api.github.com/user").json()
    return {"user": user}

# 認証済みAPIエンドポイント
@router.get("/user", response_model=user_schema.User)
def read_user(user: user_model.User = Depends(certification_crud.get_current_user)):
    return user_crud.convert_usermodel_to_user(user)

@router.get('/items/')
async def read_items(token: str = Depends(oauth2_scheme)):
    return {'token': token}