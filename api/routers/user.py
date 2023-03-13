from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.user as user_crud
from api.db import get_db

import api.schemas.user as user_schema

router = APIRouter()



@router.get('/users', response_model=List[user_schema.User])
async def list_users(db: AsyncSession = Depends(get_db)):
    users_list: List[user_schema.User] = []
    for user in await user_crud.get_users(db):
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

@router.get('/users/{user_id}', response_model=user_schema.User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user(db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    names = user.name.split(', ')
    regions = user.region.split(', ')
    
    return user_schema.User(
        id=user.id,
        name=user_schema.Name(first=names[0], last=names[1]),
        age=user.age,
        sex=user.sex,
        region=user_schema.Region(prefecture=regions[0], city=regions[1]),
        github_id=user.github_id,
        language=user_schema.Language(favorite=user.favorite_langs.split(', '), want_to=user.want_to_langs.split(', '))
    )

@router.post('/users', response_model=user_schema.UserCreateResponse)
async def create_user(
    user_body: user_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    user = await user_crud.create_user(db, user_body)

    names = (user.name).split(', ')
    regions = (user.region).split(', ')

    return user_schema.UserCreateResponse(
        id=user.id,
        name=user_schema.Name(first=names[0], last=names[1]),
        age=user.age,
        sex=user.sex,
        region=user_schema.Region(prefecture=regions[0], city=regions[1]),
        github_id=user.github_id,
        language=user_schema.Language(favorite=(user.favorite_langs).split(', '), want_to=(user.want_to_langs).split(', '))
    )


@router.put('/users/{user_id}', response_model=user_schema.UserCreateResponse)
async def update_user(
    user_id: int, user_body: user_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='Task not found')
    
    updated_user = await user_crud.update_person(db, user_body, original=user)

    names = (updated_user.name).split(', ')
    regions = (updated_user.region).split(', ')

    return user_schema.UserCreateResponse(
        id=updated_user.id,
        name=user_schema.Name(first=names[0], last=names[1]),
        age=updated_user.age,
        sex=updated_user.sex,
        region=user_schema.Region(prefecture=regions[0], city=regions[1]),
        github_id=updated_user.github_id,
        language=user_schema.Language(favorite=(updated_user.favorite_langs).split(', '), want_to=(updated_user.want_to_langs).split(', '))
    )

@router.delete('/users/{user_id}', response_model=None)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    return await user_crud.delete_user(db, original=user)

@router.get('/matching/{user_id}', response_model=List[user_schema.User])
async def matching_users(user_id: int, db: AsyncSession = Depends(get_db)):
    pass

