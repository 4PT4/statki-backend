from datetime import datetime
from tokenize import _Position
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base



class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(20))
    wins = Column(Integer)
    loses = Column(Integer)
    warships = Column(list)
    last_seen = Column(datetime)

   # owner = relationship("User", back_populates="items")

class Warship(Base):
    __tablename__="warship"
    id = Column(Integer, primary_key=True, index=True )
    position = Column(_Position)
    length = Column(Integer)
    orientation = Column(Orientation)

class Position(Base):
    __tablename__="position"
    id = Column(Integer, primary_key=True, index=True )
    x = Column(Integer)
    y = Column(Integer)

class Orientation(Base):
    __tablename__="orientation"
    id = Column(Integer, primary_key=True, index=True )
    vertical = Column(Integer)
    horizontal = Column(Integer)


