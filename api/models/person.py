from sqlalchemy import Column, Integer, String, types

from typing import Optional
from api.schemas.person import Name

from api.db import Base


class NameType(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, name: Name, dialect):
        return f"{name.first} {name.last}"

    def process_result_value(self, name: Optional[str], dialect):
        if name is None:
            return None
        first, last = name.split(" ")
        return Name(first=first, last=last)


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True)
    name = Column(NameType(60), nullable=True)
    region_prefecture = Column(String(30))
    region_city = Column(String(30))
    favorite_lang_00 = Column(String(30))
    favorite_lang_01 = Column(String(30))
    favorite_lang_02 = Column(String(30))
    favorite_lang_03 = Column(String(30))
    favorite_lang_04 = Column(String(30))