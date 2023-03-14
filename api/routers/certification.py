from fastapi import APIRouter

router = APIRouter()



@router.get('/login/github')
async def login_github():
    pass

@router.get('/login/github/callback')
async def login_github_callback():
    pass