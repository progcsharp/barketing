from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, \
    Integer, String, Boolean, MetaData

from .utils import conventions


meta = MetaData(naming_convention=conventions)

Base = declarative_base(metadata=meta)


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    nickname = Column(String)
    pay_course = Column(Integer)

    def __init__(self, tg_id, nickname):
        self.tg_id = tg_id
        self.nickname = nickname


class Link(Base):
    __tablename__ = "Link"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    count = Column(Integer)
    name = Column(String)

    def __init__(self, url, name):
        self.url = url
        self.count = 0
        self.name = name


class Message(Base):
    __tablename__ = "Message"

    id = Column(Integer, primary_key=True)
    slug = Column(String)
    message = Column(String)
    title = Column(String)

    def __init__(self, slug, message):
        self.slug = slug
        self.message = message
