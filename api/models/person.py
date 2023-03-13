from sqlalchemy import Column, Integer, String

from api.db import Base


class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True)
    name = Column(String(62))
    age = Column(Integer)
    sex = Column(Integer)
    region = Column(String(62))
    github_id = Column(String(40))
    favorite_langs = Column(String(158))
    want_to_langs = Column(String(158))
