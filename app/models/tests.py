from sqlalchemy import Column, Integer, Text
from app.db import Base


class Test:
    id = Column(Integer, primary_key=True)
    questions = Column(Text) 
    answers = Column(Text)

class Keyrsi(Base, Test):
    __tablename__ = "keyrsi"

class Tomas(Base, Test):
    __tablename__ = "tomas"

class Motivacionniy(Base, Test):
    __tablename__ = "motivacionniy"