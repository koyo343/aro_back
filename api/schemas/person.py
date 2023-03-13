from typing import Optional, List

from pydantic import BaseModel, Field


class Name(BaseModel):
    first: Optional[str] = Field(None, example='太郎')
    last: Optional[str] = Field(None, example='飯塚')

class Region(BaseModel):
    prefecture: Optional[str] = Field(None, example='福岡')
    city: Optional[str] = Field(None, example='飯塚')

class PersonBase(BaseModel):
    name: Optional[Name] = Field(None, example=Name(first='太郎', last='飯塚'))
    region: Optional[Region] = Field(None, example=Region(prefecture='福岡', city='飯塚'))
    favorite_language: Optional[List[str]] = Field(None, example=['Python'])

class PersonCreate(PersonBase):
    pass

class PersonCreateResponse(PersonCreate):
    id: int

    class Config:
        orm_mode = True

class Person(PersonBase):
    id: int
    
    class Config:
        orm_mode = True
