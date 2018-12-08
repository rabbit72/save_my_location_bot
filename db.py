import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, ForeignKey

DATABASE_URL = os.getenv("DATABASE_URL") or open("../DB_TOKEN.txt").read()
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    latitude = Column(Float)
    longitude = Column(Float)
    image = Column(String(64), nullable=True)
    description = Column(String(256), nullable=True)
    owner = Column(ForeignKey("user.id"))

    def __init__(self, name, coordinates, image=None, description=None, owner=None):
        self.name = name
        self.latitude, self.longitude = coordinates
        self.image = image
        self.description = description
        self.owner = owner

    def __repr__(self):
        pass  # TODO


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def add_location(self, name, coordinates, image=None, description=None):
        location = Location(name, coordinates, image, description, owner=self.id)
        session.add(location)
        session.commit()

    @property
    def locations(self):
        r = session.query(Location).filter(Location.owner == self.id)
        return list(r)

    def __repr__(self):
        pass  # TODO


Base.metadata.create_all(engine)


if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session = Session()
    # user = User(34534543)
    # session.add(user)
    # session.commit()
    # user.add_location("ddsd", [54.23424, 55.43434])
    user = session.query(User).get(2)
    print(user)
    print(user.locations[0].owner)

