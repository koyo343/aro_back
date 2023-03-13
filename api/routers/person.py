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
        id, first, last, age, sex, prefecture, city, lang_0, lang_1, lang_2, lang_3, lang_4 = person 
        persons_list.append(person_schema.Person(
                                    id=id,
                                    name=person_schema.Name(first=first, last=last),
                                    age=age,
                                    sex=sex,
                                    region=person_schema.Region(prefecture=prefecture, city=city),
                                    favorite_language=[
                                        lang_0, lang_1, lang_2, lang_3, lang_4
                                    ]
                                ))
    
    return persons_list

@router.post('/persons', response_model=person_schema.PersonCreateResponse)
async def create_person(
    person_body: person_schema.PersonCreate, db: AsyncSession = Depends(get_db)
):
    person = await person_crud.create_person(db, person_body)

    return person_schema.PersonCreateResponse(
        id=person.id,
        name=person_schema.Name(first=person.first_name, last=person.last_name),
        age=person.age,
        sex=person.sex,
        region=person_schema.Region(prefecture=person.region_prefecture, city=person.region_city),
        favorite_language=[
            person.favorite_lang_00,
            person.favorite_lang_01,
            person.favorite_lang_02,
            person.favorite_lang_03,
            person.favorite_lang_04
        ]
    )


@router.put('/persons/{person_id}', response_model=person_schema.PersonCreateResponse)
async def update_person(
    person_id: int, person_body: person_schema.PersonCreate, db: AsyncSession = Depends(get_db)
):
    person = await person_crud.get_person(db, person_id=person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    updated_person = await person_crud.update_person(db, person_body, original=person)

    return person_schema.PersonCreateResponse(
        id=updated_person.id,
        name=person_schema.Name(first=updated_person.first_name, last=updated_person.last_name),
        age=updated_person.age,
        sex=updated_person.sex,
        region=person_schema.Region(prefecture=updated_person.region_prefecture, city=updated_person.region_city),
        favorite_language=[
            updated_person.favorite_lang_00,
            updated_person.favorite_lang_01,
            updated_person.favorite_lang_02,
            updated_person.favorite_lang_03,
            updated_person.favorite_lang_04
        ]
    )

@router.delete("/persons/{person_id}", response_model=None)
async def delete_person(person_id: int, db: AsyncSession = Depends(get_db)):
    person = await person_crud.get_person(db, person_id=person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return await person_crud.delete_person(db, original=person)
