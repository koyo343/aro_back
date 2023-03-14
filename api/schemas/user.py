from typing import Optional, List

from pydantic import BaseModel, Field


class Name(BaseModel):
    first: Optional[str] = Field(None, example='太郎')
    last: Optional[str] = Field(None, example='飯塚')

class Region(BaseModel):
    prefecture: Optional[str] = Field(None, example='福岡')
    city: Optional[str] = Field(None, example='飯塚')

class Language(BaseModel):
    favorite: Optional[List[str]] = Field(None, example=['Python', '', '', '', ''])
    want_to: Optional[List[str]] = Field(None, example=['C++', '', '', '', ''])

class UserBase(BaseModel):
    name: Optional[Name] = Field(None, example=Name(first='太郎', last='飯塚'))
    age: Optional[int] = Field(None, example=19)
    sex: Optional[int] = Field(None, example=0)
    region: Optional[Region] = Field(None, example=Region(prefecture='福岡', city='飯塚'))
    github_id: Optional[str] = Field(None, example='tarou11')
    language: Optional[Language] = Field(None, example=Language(favorite=['Python', '', '', '', ''], want_to=['C++', '', '', '', '']))


class UserCreate(UserBase):
    password: Optional[str]

class UserCreateResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    password: Optional[str]
    
    class Config:
        orm_mode = True

class UserWithPassword(User):
    password: Optional[str]
