from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.searching as searching_crud
from api.db import get_db

import api.schemas.user as user_schema

router = APIRouter()

@router.get('/search/', response_model=List[user_schema.User])
async def search_user(
    name: Optional[str] = None, age: Optional[int] = None, sex: Optional[int] = None, prefecture: Optional[str] = None, city: Optional[str] = None, githubid: Optional[str] = None, 
    favolangs: Optional[str] = None,
    wantlangs: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
) -> List[user_schema.User]:
    return await searching_crud.search_user(
        db=db, name=name, age=age, sex=sex, prefecture=prefecture, city=city, 
        githubid=githubid, 
        favolangs=favolangs.split(',') if favolangs is not None else None, 
        wantlangs=wantlangs.split(',') if wantlangs is not None else None
    )