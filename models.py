from datetime import datetime
from tokenize import _Position
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, enum
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

class Orientation(enum.Enum):
    horizontal = 1
    vertical = 2
    

class Warship(Base):
    __tablename__="warship"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer)
    position = Column(_Position)
    length = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    orientation = Column(enum(Orientation))





