from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
from entities import Orientation
from utils import get_current_timestamp, get_uuid


class Player(Base):
    __tablename__ = "player"
    id = Column(String(36), primary_key=True, index=True, default=get_uuid)
    nickname = Column(String(20), index=True)
    password = Column(String(255))
    wins = Column(Integer, default=0)
    loses = Column(Integer, default=0)
    win_streak = Column(Integer, default=0)
    last_seen = Column(Integer, default=get_current_timestamp)

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
