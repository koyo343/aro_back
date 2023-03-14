from sqlalchemy import Column, Integer, String

from api.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    password = Column(String(64))
    name = Column(String(62))
    age = Column(Integer)
    sex = Column(Integer)
    region = Column(String(62))
    github_id = Column(String(40))
    favorite_langs = Column(String(158))
    want_to_langs = Column(String(158))
    profile_sentence = Column(String(500))
