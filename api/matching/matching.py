from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.person import Person

class PersonWithValue:
    def __init__(self, value: int, person: Person) -> None:
        self.value: int = value
        self.person: Person = person

async def evaluate_degree_of_match(person: Person, other_person: Person) -> int:
    person.language.want_to

async def matching_persons(
        db: AsyncSession, person: Person, num: int
):
    pass