from fastapi import APIRouter, Depends
# from requests_oauthlib import OAuth2Session
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

CLIENT_ID = 'b811937cf10d9b379129'
CLIENT_SECRET = '3b461ccaf29125635461541f506e175a20f15d32'

# github = OAuth2Session(CLIENT_ID, redirect_uri='http://localhost:8000/callback/github')

@router.get('/items/')
async def read_items(token: str = Depends(oauth2_scheme)):
    return {'token': token}

# @router.get('/login/github')
# async def login_github():
#     pass

# @router.get('/login/github/callback')
# async def login_github_callback():
#     pass