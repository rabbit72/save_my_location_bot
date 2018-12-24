import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, ForeignKey

DATABASE_URL = os.getenv("DATABASE_URL") or open("../DB_TOKEN.txt").read()
engine = create_engine(DATABASE_URL, echo=False)

Base = declarative_base()


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    title = Column(String(32))
    latitude = Column(Float)
    longitude = Column(Float)
    image = Column(String(64), nullable=True)
    description = Column(String(256), nullable=True)
    owner = Column(ForeignKey("user.id"))

    def __init__(
        self,
        title=None,
        latitude=None,
        longitude=None,
        image=None,
        description=None,
        owner=None,
    ):
        self.title = title
        self.latitude = latitude
        self.longitude = longitude
        self.image = image
        self.description = description
        self.owner = owner

    def __repr__(self):
        return f"Location <{self.latitude}, {self.longitude}>"


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    stage = Column(Integer, default=0)

    def __init__(self, chat_id):
        self.id = chat_id

    def add_location(self, location: Location):
        location.owner = self.id
        session.add(location)
        session.commit()

    def change_stage(self, stage: int):
        self.stage = stage
        session.commit()

    def delete_all_locations(self):
        session.query(Location).filter(Location.owner == self.id).delete()
        session.commit()

    @property
    def locations(self):
        r = (
            session.query(Location)
            .filter(Location.owner == self.id)
            .order_by(Location.id.desc())
            .limit(10)
        )
        return list(r)

    def __repr__(self):
        return f"User <id: {self.id}>"


def get_user(message):
    chat_id = message.chat.id
    current_user = session.query(User).get(chat_id)
    if not current_user:
        current_user = User(chat_id)
        session.add(current_user)
        session.commit()
    return current_user


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
