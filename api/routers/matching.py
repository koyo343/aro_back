from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.matching as matching_crud
from api.db import get_db

import api.schemas.user as user_schema

router = APIRouter()

@router.get('/matching/{user_id}', response_model=List[user_schema.User])
async def matching_users(user_id: int, startindex: int = 0, num: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    return await matching_crud.matching_users(db, user_id, startindex, num)
