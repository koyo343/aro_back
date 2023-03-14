from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Optional

import api.schemas.user as user_schema
import api.cruds.user as user_crud

def __judge_equal(value, user_data) -> bool:
    if value == None:
        return False
    elif value == user_data:
        return True
    else:
        return False
    
def __judge_part_equal(value, user_data) -> bool:
    if value == None:
        return False
    elif value in user_data:
        return True
    else:
        return False

async def search_user(
    db: AsyncSession, name: Optional[str], age: Optional[int], sex: Optional[int], prefecture: Optional[str], city: Optional[str], 
    githubid: Optional[str], favolangs: Optional[List[str]], wantlangs: Optional[List[str]]
) -> List[user_schema.User]:
    users_list = await user_crud.list_users(db)
    if name != None:
        if len(users_list) == 0:
            return []
        for i, user in enumerate(users_list):
            if not __judge_part_equal(name, user.name.last + user.name.first):
                users_list[i] = None
        users_list = [u for u in users_list if u is not None]
    if age != None:
        if len(users_list) == 0:
            return []
        for i, user in enumerate(users_list):
            if not __judge_equal(age, user.age):
                users_list[i] = None
        users_list = [u for u in users_list if u is not None]
    if sex != None:
        if len(users_list) == 0:
            return []
        for i, user in enumerate(users_list):
            if not __judge_equal(sex, user.sex):
                users_list[i] = None
        users_list = [u for u in users_list if u is not None]
    if prefecture != None:
        if len(users_list) == 0:
            return []
        for i, user in enumerate(users_list):
            if not __judge_equal(prefecture, user.region.prefecture):
                users_list[i] = None
        users_list = [u for u in users_list if u is not None]
    if city != None:
        if len(users_list) == 0:
            return []
        for i, user in enumerate(users_list):
            if not __judge_equal(city, user.region.city):
                users_list[i] = None
        users_list = [u for u in users_list if u is not None]
    if githubid != None:
        if len(users_list) == 0:
            return []
        for i, user in enumerate(users_list):
            if not __judge_part_equal(githubid, user.github_id):
                users_list[i] = None
        users_list = [u for u in users_list if u is not None]
    if favolangs != None:
        for lang in favolangs:
            if lang != None:
                if len(users_list) == 0:
                    return []
                for i, user in enumerate(users_list):
                    if user == None:
                        continue
                    if not __judge_part_equal(lang, user.language.favorite):
                        users_list[i] = None
                    print(i)
        users_list = [u for u in users_list if u is not None]
    if wantlangs != None:
        for lang in wantlangs:
            if lang != None:
                if len(users_list) == 0:
                    return []
                for i, user in enumerate(users_list):
                    if user == None:
                        continue
                    if not __judge_part_equal(lang, user.language.want_to):
                        users_list[i] = None
        users_list = [u for u in users_list if u is not None]

    return users_list