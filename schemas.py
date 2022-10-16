from datetime import datetime
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
    warship_id: int
    player_id: int
    length:  int
    x: int
    y: int
    orientation: int
    class Config:
        orm_mode = True
 

