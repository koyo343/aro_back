from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

from typing import List, Tuple, Optional

import api.models.user as user_model
import api.schemas.user as user_schema


async def create_user(
    db: AsyncSession, user_create: user_schema.UserCreate
) -> user_model.User:
    user = user_model.User(
        name = user_create.name.first + ', ' + user_create.name.last,
        age = user_create.age,
        sex = user_create.sex,
        region = user_create.region.prefecture + ', ' + user_create.region.city,
        github_id = user_create.github_id,
        favorite_langs = ', '.join(user_create.language.favorite),
        want_to_langs = ', '.join(user_create.language.want_to)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_users(db: AsyncSession) -> List[Tuple[int, str]]:
    result: Result = await (
        db.execute(
            select(
                user_model.User.id,
                user_model.User.name,
                user_model.User.age,
                user_model.User.sex,
                user_model.User.region,
                user_model.User.github_id,
                user_model.User.favorite_langs,
                user_model.User.want_to_langs
            )
        )
    )

    return result.all()

async def list_users(db: AsyncSession) -> List[user_schema.User]:
    users_list: List[user_schema.User] = []
    users = await get_users(db)
    for user in users:
        id, name, age, sex, region, github_id, fav_lang, want_lang = user 
        names = name.split(', ')
        regions = region.split(', ')
        users_list.append(user_schema.User(
                                    id=id,
                                    name=user_schema.Name(first=names[0], last=names[1]),
                                    age=age,
                                    sex=sex,
                                    region=user_schema.Region(prefecture=regions[0], city=regions[1]),
                                    github_id=github_id,
                                    language=user_schema.Language(favorite=fav_lang.split(', '), want_to=want_lang.split(', '))
                                ))
    
    return users_list

async def get_user(db: AsyncSession, user_id: int) -> Optional[user_model.User]:
    result: Result = await db.execute(
        select(user_model.User).filter(user_model.User.id == user_id)
    )
    user: Optional[Tuple[user_model.User]] = result.first()
    return user[0] if user is not None else None

def convert_usermodel_to_user(user_model: user_model.User) -> user_schema.User:
    names = user_model.name.split(', ')
    regions = user_model.region.split(', ')
    
    return user_schema.User(
        id=user_model.id,
        name=user_schema.Name(first=names[0], last=names[1]),
        age=user_model.age,
        sex=user_model.sex,
        region=user_schema.Region(prefecture=regions[0], city=regions[1]),
        github_id=user_model.github_id,
        language=user_schema.Language(favorite=user_model.favorite_langs.split(', '), want_to=user_model.want_to_langs.split(', '))
    )

def convert_usermodel_to_user_create_response(user_model: user_model.User) -> user_schema.UserCreateResponse:
    names = user_model.name.split(', ')
    regions = user_model.region.split(', ')
    
    return user_schema.UserCreateResponse(
        id=user_model.id,
        name=user_schema.Name(first=names[0], last=names[1]),
        age=user_model.age,
        sex=user_model.sex,
        region=user_schema.Region(prefecture=regions[0], city=regions[1]),
        github_id=user_model.github_id,
        language=user_schema.Language(favorite=user_model.favorite_langs.split(', '), want_to=user_model.want_to_langs.split(', '))
    )

async def update_person(
        db: AsyncSession, user_create: user_schema.UserCreate, original: user_model.User
) -> user_model.User:
    original.name = user_create.name.first + ', ' + user_create.name.last
    original.age = user_create.age
    original.sex = user_create.sex
    original.region = user_create.region.prefecture + ', ' + user_create.region.city
    original.github_id = user_create.github_id
    original.favorite_langs = ', '.join(user_create.language.favorite)
    original.want_to_langs = ', '.join(user_create.language.want_to)

    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def delete_user(db: AsyncSession, original: user_model.User) -> None:
    await db.delete(original)
    await db.commit()