from fastapi import FastAPI, Request
from oauthlib.oauth2 import TokenExpiredError
from starlette.responses import RedirectResponse

from api.routers import user, matching, searching, certification

app = FastAPI()

app.include_router(user.router)
app.include_router(matching.router)
app.include_router(searching.router)
app.include_router(certification.router)

# アクセストークンの有効期限切れなどのエラーが発生した場合には認証画面にリダイレクト
@app.exception_handler(TokenExpiredError)
async def handle_token_expired_error(request: Request, exc: TokenExpiredError):
    return RedirectResponse(url="/login/github")