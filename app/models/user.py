from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base
from app.models.results import TestResult
from app.models.refresh_token import RefreshToken


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    last_name = Column(String)
    username = Column(String)
    hashed_password = Column(String)

    test_results = relationship("TestResult", back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")