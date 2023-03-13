from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.person as person_crud
from api.db import get_db

import api.schemas.person as person_schema

router = APIRouter()



@router.get('/persons', response_model=List[person_schema.Person])
async def list_persons():
    return [person_schema.Person(
        id=1, name=person_schema.Name(first='花子', last='小倉'), 
        region=person_schema.Region(prefecture='福岡', city='小倉'),
        favorite_language=['C++', 'Rust'])]

@router.post('/persons', response_model=person_schema.PersonCreateResponse)
async def create_person(
    person_body: person_schema.PersonCreate, db: AsyncSession = Depends(get_db)
):
    
    return await person_crud.create_person(db, person_body)


@router.put('/persons/{person_id}', response_model=person_schema.PersonCreateResponse)
async def update_person(person_id: int, person_body: person_schema.PersonCreate):
    return person_schema.PersonCreateResponse(person_id, **person_body.dict())


@router.delete("/persons/{person_id}", response_model=None)
async def delete_person(person_id: int):
    return