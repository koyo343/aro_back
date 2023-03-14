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

def judge_equal(value, user_data) -> bool:
    if value == None:
        return False
    elif value == user_data:
        return True
    else:
        return False
    
def judge_part_equal(value, user_data) -> bool:
    if value == None:
        return False
    elif value in user_data:
        return True
    else:
        return False

async def search_user(
    db: AsyncSession, name: Optional[str], age: Optional[int], sex: Optional[int], prefecture: Optional[str], city: Optional[str], 
    githubid: Optional[str], favolang: Optional[str], wantlang: Optional[str]
) -> List[user_schema.User]:
    users_list = await list_users(db)
    if name != None:
        for i, user in enumerate(users_list):
            if not judge_part_equal(name, user.name.last + user.name.first):
                users_list[i] = None
        users_list = [u for u in users_list if u is not None]
    if age != None:
        for i, user in enumerate(users_list):
            if not judge_equal(age, user.age):
                users_list[i] = None
        users_list = [u for u in users_list if u is not None]
    if sex != None:
        for i, user in enumerate(users_list):
            if not judge_equal(sex, user.sex):
                users_list[i] = None
        users_list = [u for u in users_list if u is not None]
    if prefecture != None:
        for i, user in enumerate(users_list):
            if not judge_equal(prefecture, user.region.prefecture):
                users_list[i] = None
        users_list = [u for u in users_list if u is not None]
    if city != None:
        for i, user in enumerate(users_list):
            if not judge_equal(city, user.region.city):
                users_list[i] = None
        users_list = [u for u in users_list if u is not None]
    if githubid != None:
        for i, user in enumerate(users_list):
            if not judge_part_equal(githubid, user.github_id):
                users_list[i] = None
        users_list = [u for u in users_list if u is not None]
    if favolang != None:
        for i, user in enumerate(users_list):
            if not judge_part_equal(favolang, user.language.favorite):
                users_list[i] = None
        users_list = [u for u in users_list if u is not None]
    if wantlang != None:
        for i, user in enumerate(users_list):
            if not judge_part_equal(wantlang, user.language.want_to):
                users_list[i] = None
        users_list = [u for u in users_list if u is not None]

    return users_list