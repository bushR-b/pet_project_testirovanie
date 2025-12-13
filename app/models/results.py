from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base


class TestResult(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id')) # Внешний ключ к User
    test = Column(String)
    result = Column(String)

    user = relationship("User", back_populates="test_results")
    