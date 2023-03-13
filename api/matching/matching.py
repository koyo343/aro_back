from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from api.schemas.user import User

class UserWithValue:
    def __init__(self, value: int, person: User) -> None:
        self.value: int = value
        self.person: User = person

async def evaluate_degree_of_match(user: User, other_user: User) -> int:
    user.language.want_to

async def matching_users(
        db: AsyncSession, user: User, num: int
) -> List[User]:
    pass