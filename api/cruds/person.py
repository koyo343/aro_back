from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

from typing import List, Tuple

import api.models.person as person_model
import api.schemas.person as person_schema


async def create_person(
    db: AsyncSession, person_create: person_schema.PersonCreate
) -> person_model.Person:
    person = person_model.Person(
        first_name = person_create.name.first,
        last_name = person_create.name.last,
        age = person_create.age,
        sex = person_create.sex,
        region_prefecture = person_create.region.prefecture,
        region_city = person_create.region.city,
        favorite_lang_00 = person_create.favorite_language[0],
        favorite_lang_01 = person_create.favorite_language[1],
        favorite_lang_02 = person_create.favorite_language[2],
        favorite_lang_03 = person_create.favorite_language[3],
        favorite_lang_04 = person_create.favorite_language[4]
    )
    db.add(person)
    await db.commit()
    await db.refresh(person)
    return person

async def get_persons(db: AsyncSession) -> List[Tuple[int, str]]:
    result: Result = await (
        db.execute(
            select(
                person_model.Person.id,
                person_model.Person.first_name,
                person_model.Person.last_name,
                person_model.Person.age,
                person_model.Person.sex,
                person_model.Person.region_prefecture,
                person_model.Person.region_city,
                person_model.Person.favorite_lang_00,
                person_model.Person.favorite_lang_01,
                person_model.Person.favorite_lang_02,
                person_model.Person.favorite_lang_03,
                person_model.Person.favorite_lang_04 
            )
        )
    )

    return result.all()