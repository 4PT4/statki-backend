from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from database import Base
from utils import get_current_timestamp, get_uuid
import enum


class Orientation(enum.Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Player(Base):
    __tablename__ = "player"
    id = Column(String(36), primary_key=True, index=True, default=get_uuid)
    nickname = Column(String(20), index=True)
    password = Column(String(255))
    wins = Column(Integer, default=0)
    loses = Column(Integer, default=0)
    last_seen = Column(Integer, default=get_current_timestamp)
    warships = relationship("Warship")


class Warship(Base):
    __tablename__ = "warship"
    id = Column(String(36), primary_key=True, index=True, default=get_uuid)
    player_id = Column(String(36), ForeignKey("player.id"))
    x = Column(Integer)
    y = Column(Integer)
    length = Column(Integer)
    orientation = Column(Enum(Orientation))