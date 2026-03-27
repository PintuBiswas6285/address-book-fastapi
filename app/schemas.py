# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from sqlalchemy import Column, Integer, String, Float
from .database import Base

# Address table definition
class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
