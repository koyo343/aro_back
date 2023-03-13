from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

from typing import List, Tuple, Optional

import api.models.person as person_model
import api.schemas.person as person_schema


async def create_person(
    db: AsyncSession, person_create: person_schema.PersonCreate
) -> person_model.Person:
    person = person_model.Person(
        name = person_create.name.first + ', ' + person_create.name.last,
        age = person_create.age,
        sex = person_create.sex,
        region = person_create.region.prefecture + ', ' + person_create.region.city,
        github_id = person_create.github_id,
        favorite_langs = ', '.join(person_create.language.favorite),
        want_to_langs = ', '.join(person_create.language.want_to)
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
                person_model.Person.name,
                person_model.Person.age,
                person_model.Person.sex,
                person_model.Person.region,
                person_model.Person.github_id,
                person_model.Person.favorite_langs,
                person_model.Person.want_to_langs
            )
        )
    )

    return result.all()

async def get_person(db: AsyncSession, person_id: int) -> Optional[person_model.Person]:
    result: Result = await db.execute(
        select(person_model.Person).filter(person_model.Person.id == person_id)
    )
    person: Optional[Tuple[person_model.Person]] = result.first()
    return person[0] if person is not None else None

async def update_person(
        db: AsyncSession, person_create: person_schema.PersonCreate, original: person_model.Person
) -> person_model.Person:
    original.name = person_create.name.first + ', ' + person_create.name.last
    original.age = person_create.age
    original.sex = person_create.sex
    original.region = person_create.region.prefecture + ', ' + person_create.region.city
    original.github_id = person_create.github_id
    original.favorite_langs = ', '.join(person_create.language.favorite)
    original.want_to_langs = ', '.join(person_create.language.want_to)

    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def delete_person(db: AsyncSession, original: person_model.Person) -> None:
    await db.delete(original)
    await db.commit()