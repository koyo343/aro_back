from fastapi import FastAPI

from api.routers import person

app = FastAPI()

app.include_router(person.router)