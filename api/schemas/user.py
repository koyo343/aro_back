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
    profile_sentence: Optional[str] = Field(None, example='飯塚太郎です。\nI\'m a Tarou Iizuka.')


class UserCreate(UserBase):
    password: str = Field('password', example='password')

class UserCreateResponse(UserBase):
    id: int
    disabled: Optional[int]

    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    pass

class UserUpdateResponse(UserBase):
    id: int
    disabled: Optional[int]

    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    disabled: Optional[int]
    
    class Config:
        orm_mode = True

class UserWithPassword(User):
    hashed_password: Optional[str]
