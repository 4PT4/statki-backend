import enum
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Date
from sqlalchemy.orm import relationship
from database import Base

class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(20))
    wins = Column(Integer)
    loses = Column(Integer)
    last_seen = Column(Date)

    player_relation = relationship("Warship", back_populates="warship_relation")


class Orientation(enum.Enum):
    horizontal = 1
    vertical = 2
   

class Warship(Base):
    __tablename__="warship"
    warship_id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("player.id"))
    length = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    orientation = Column(Enum(Orientation))

    warship_relation = relationship("Player", back_populates="player_relation")

    #orientation = Column(Boolean)
    # 0 equals horizonta, 1 equals vertical