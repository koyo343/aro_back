from fastapi import FastAPI

from api.routers import user, matching, searching

app = FastAPI()

app.include_router(user.router)
app.include_router(matching.router)
app.include_router(searching.router)