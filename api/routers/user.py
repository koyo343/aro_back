from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.user as user_crud
from api.db import get_db

import api.schemas.user as user_schema

router = APIRouter()



@router.get('/users', response_model=List[user_schema.User])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await user_crud.list_users(db)

@router.get('/users/{user_id}', response_model=user_schema.User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user(db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    return user_crud.convert_usermodel_to_user(user)

@router.post('/users', response_model=user_schema.UserCreateResponse)
async def create_user(
    user_body: user_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    user = await user_crud.create_user(db, user_body)

    return user_crud.convert_usermodel_to_user_create_response(user)


@router.put('/users/{user_id}', response_model=user_schema.UserUpdateResponse)
async def update_user(
    user_id: int, user_body: user_schema.UserUpdate, db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    updated_user = await user_crud.update_person(db, user_body, original=user)

    return user_crud.convert_usermodel_to_user_create_response(updated_user)

@router.delete('/users/{user_id}', response_model=None)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    return await user_crud.delete_user(db, original=user)