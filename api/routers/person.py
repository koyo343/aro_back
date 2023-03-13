from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.person as person_crud
from api.db import get_db

import api.schemas.person as person_schema

router = APIRouter()



@router.get('/persons', response_model=List[person_schema.Person])
async def list_persons(db: AsyncSession = Depends(get_db)):
    persons_list: List[person_schema.Person] = []
    for person in await person_crud.get_persons(db):
        id, name, age, sex, region, github_id, fav_lang, want_lang = person 
        names = name.split(', ')
        regions = region.split(', ')
        persons_list.append(person_schema.Person(
                                    id=id,
                                    name=person_schema.Name(first=names[0], last=names[1]),
                                    age=age,
                                    sex=sex,
                                    region=person_schema.Region(prefecture=regions[0], city=regions[1]),
                                    github_id=github_id,
                                    language=person_schema.Language(favorite=fav_lang.split(', '), want_to=want_lang.split(', '))
                                ))
    
    return persons_list

@router.get('/person/{person_id}', response_model=person_schema.Person)
async def get_person(person_id: int, db: AsyncSession = Depends(get_db)):
    person = await person_crud.get_person(db, person_id=person_id)

    if person is None:
        raise HTTPException(status_code=404, detail='Task not found')
    
    names = person.name.split(', ')
    regions = person.region.split(', ')
    
    return person_schema.Person(
        id=person.id,
        name=person_schema.Name(first=names[0], last=names[1]),
        age=person.age,
        sex=person.sex,
        region=person_schema.Region(prefecture=regions[0], city=regions[1]),
        github_id=person.github_id,
        language=person_schema.Language(favorite=person.favorite_langs.split(', '), want_to=person.la.split(', '))
    )

@router.post('/persons', response_model=person_schema.PersonCreateResponse)
async def create_person(
    person_body: person_schema.PersonCreate, db: AsyncSession = Depends(get_db)
):
    person = await person_crud.create_person(db, person_body)

    names = (person.name).split(', ')
    regions = (person.region).split(', ')

    return person_schema.PersonCreateResponse(
        id=person.id,
        name=person_schema.Name(first=names[0], last=names[1]),
        age=person.age,
        sex=person.sex,
        region=person_schema.Region(prefecture=regions[0], city=regions[1]),
        github_id=person.github_id,
        language=person_schema.Language(favorite=(person.favorite_langs).split(', '), want_to=(person.want_to_langs).split(', '))
    )


@router.put('/persons/{person_id}', response_model=person_schema.PersonCreateResponse)
async def update_person(
    person_id: int, person_body: person_schema.PersonCreate, db: AsyncSession = Depends(get_db)
):
    person = await person_crud.get_person(db, person_id=person_id)
    if person is None:
        raise HTTPException(status_code=404, detail='Task not found')
    
    updated_person = await person_crud.update_person(db, person_body, original=person)

    names = (updated_person.name).split(', ')
    regions = (updated_person.region).split(', ')

    return person_schema.PersonCreateResponse(
        id=updated_person.id,
        name=person_schema.Name(first=names[0], last=names[1]),
        age=updated_person.age,
        sex=updated_person.sex,
        region=person_schema.Region(prefecture=regions[0], city=regions[1]),
        github_id=updated_person.github_id,
        language=person_schema.Language(favorite=(updated_person.favorite_langs).split(', '), want_to=(updated_person.want_to_langs).split(', '))
    )

@router.delete('/persons/{person_id}', response_model=None)
async def delete_person(person_id: int, db: AsyncSession = Depends(get_db)):
    person = await person_crud.get_person(db, person_id=person_id)
    if person is None:
        raise HTTPException(status_code=404, detail='Task not found')
    
    return await person_crud.delete_person(db, original=person)

@router.get('/matching/{person_id}', response_model=List[person_schema.Person])
async def matching_persons(person_id: int, db: AsyncSession = Depends(get_db)):
    pass

