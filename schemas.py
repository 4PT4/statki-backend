from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Union

class Message(BaseModel):
    event: str
    data: object


#code for database

class PlayerBase(BaseModel):
    id: int 
    nickname: Union[str, None] = None
    wins: int
    loses: int
    last_seen: datetime
    class Config: 
        orm_mode = True

class WarshipBase(BaseModel):
    id: int
    player_id: int
    length:  int
    x: int
    y: int
    orientation: Enum
    class Config:
        orm_mode = True
 

