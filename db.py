import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from geoalchemy2 import Geometry

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

Base = declarative_base()


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    coordinates = Column(Geometry('POINT'))
    image = Column(String(64), nullable=True)
    description = Column(String(256), nullable=True)

    def __init__(self, name, coordinates, image=None, description=None):
        self.name = name
        self.coordinates = coordinates
        self.image = image
        self.description = description


Base.metadata.create_all(engine)
