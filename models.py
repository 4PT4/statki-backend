from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Date
from sqlalchemy.orm import relationship
from database import Base
from entities import Orientation

# create models


class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(20))
    wins = Column(Integer)
    loses = Column(Integer)
    last_seen = Column(Date)

    player_relation = relationship(
        "Warship", back_populates="warship_relation")


class Warship(Base):
    __tablename__ = "warship"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("player.id"))
    length = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    orientation = Column(Enum(Orientation))

    warship_relation = relationship("Player", back_populates="player_relation")

    #orientation = Column(Boolean)
