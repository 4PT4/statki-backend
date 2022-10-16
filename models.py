#import enum
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

    #player_relation = relationship("Warship", back_populates="warship_relation")

    def __init__(self, id, nickname, wins, loses, last_seen):
        self.id = id
        self.nickname = nickname
        self.wins = wins
        self.loses = loses
        self.last_seen = last_seen
"""
class Orientation(enum.Enum):
    horizontal = 1
    vertical = 2
"""
   

class Warship(Base):
    __tablename__="warship"
    warship_id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer)
    length = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    #orientation = Column(Enum(Orientation))
    orientation = Column(Boolean)
    # 0 equals horizontal, 1 equals vertical

   # warship_relation = relationship("Player", back_populates="player_relation")

    #player = relationship("Player", back_populates)

    def __init__(self, warship_id, player_id ,length, x, y, orientation):
        self.warship_id = warship_id
        self.player_id = player_id
        self.length = length
        self.x = x
        self.y = y
        self.orientation = orientation


