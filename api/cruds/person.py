from sqlalchemy.ext.asyncio import AsyncSession

import api.models.person as person_model
import api.schemas.person as person_schema

from api.models.person import NameType


async def create_person(
    db: AsyncSession, person_create: person_schema.PersonCreate
) -> person_model.Person:
    person = person_model.Person(
        name = NameType.process_bind_param(None, person_create.name, None),
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