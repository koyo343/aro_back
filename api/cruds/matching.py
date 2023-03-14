from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Optional

from fastapi import HTTPException

import api.schemas.user as user_schema
import api.cruds.user as user_crud

class UserWithValueList:
    def __init__(self) -> None:
        self.values: List[int] = []
        self.users_list: List[user_schema.User] = []

    def append(self, value: int, user: user_schema.User):
        self.values.append(value)
        self.users_list.append(user)

    def sort(self, reverse: bool = False):
        indexes = list(range(len(self.values)))
        indexes.sort(key=lambda i: self.values[i], reverse=True)
        
        # valuesとusers_listを同じインデックスでソートする
        sorted_values = [self.values[i] for i in indexes]
        sorted_users = [self.users_list[i] for i in indexes]
        
        # ソートされたvaluesとusers_listを格納する
        if reverse:
            self.values = sorted_values.reverse()
            self.users_list = sorted_users.reverse()
        else:
            self.values = sorted_values
            self.users_list = sorted_users

    def append_and_sort(self, value: int, user: user_schema.User, reverse: bool = False):
        self.append(value, user)
        self.sort(reverse)

def __evaluate_degree_of_match(myself_user: user_schema.User, other_user: user_schema.User) -> int:
    value: int = 0

    myself_user_want_langs = list(set(myself_user.language.want_to))
    other_user_want_langs = list(set(other_user.language.want_to))
    for user_langs in myself_user_want_langs:
        if user_langs in other_user_want_langs:
            value += 10

    myself_user_favo_langs = list(set(myself_user.language.favorite))
    other_user_favo_langs = list(set(other_user.language.favorite))
    for user_langs in myself_user_favo_langs:
        if user_langs in other_user_favo_langs:
            value += 6

    return value

async def matching_users(
        db: AsyncSession, user_id: int, start_index: int = 0, num: Optional[int] = None
) -> List[user_schema.User]:
    user_myself_model = await user_crud.get_user(db=db, user_id=user_id)
    if user_myself_model == None:
        raise HTTPException(status_code=404, detail='User not found')
    user_myself: Optional[user_schema.User] = user_crud.convert_usermodel_to_user(user_myself_model)
    users_list = await user_crud.list_users(db)

    users_value_list = UserWithValueList()

    for user in users_list:
        if user.id == user_myself.id:
            continue
        users_value_list.append(__evaluate_degree_of_match(user_myself, user), user)

    users_value_list.sort()

    if start_index != None:
        users_value_list.users_list = users_value_list.users_list[start_index:]
    if num != None:
        users_value_list.users_list = users_value_list.users_list[:num]

    return users_value_list.users_list