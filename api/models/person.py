from sqlalchemy import Column, Integer, String

from api.db import Base


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    age = Column(Integer)
    sex = Column(Integer)
    region_prefecture = Column(String(30))
    region_city = Column(String(30))
    favorite_lang_00 = Column(String(30))
    favorite_lang_01 = Column(String(30))
    favorite_lang_02 = Column(String(30))
    favorite_lang_03 = Column(String(30))
    favorite_lang_04 = Column(String(30))