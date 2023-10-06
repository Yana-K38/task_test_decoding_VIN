from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String, unique=True, index=True)
    year = Column(Integer)
    make = Column(String)
    model = Column(String)
    type_vehicle = Column(String)
    color = Column(String)
    dimensions = Column(String)
    weight = Column(Integer)