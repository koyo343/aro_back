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
    favolang0: Optional[str] = None, favolang1: Optional[str] = None, favolang2: Optional[str] = None, favolang3: Optional[str] = None, favolang4: Optional[str] = None, 
    wantlang0: Optional[str] = None, wantlang1: Optional[str] = None, wantlang2: Optional[str] = None, wantlang3: Optional[str] = None, wantlang4: Optional[str] = None, 
    db: AsyncSession = Depends(get_db)
) -> List[user_schema.User]:
    return await searching_crud.search_user(
        db=db, name=name, age=age, sex=sex, prefecture=prefecture, city=city, 
        githubid=githubid, 
        favolangs=[favolang0, favolang1, favolang2, favolang3, favolang4], 
        wantlangs=[wantlang0, wantlang1, wantlang2, wantlang3, wantlang4]
    )