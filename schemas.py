from enum import Enum
from pydantic import BaseModel, Field
from typing import Union
from humps import camelize


class Message(BaseModel):
    event: str
    data: object


class Token(BaseModel):
    token: str


class Credentials(BaseModel):
    nickname: str
    password: str


class PlayerBase(BaseModel):
    id: str
    nickname: str
    wins: int
    loses: int
    win_streak: int = Field(alias="winStreak")
    last_seen: int = Field(alias="lastSeen")

    class Config:
        allow_population_by_field_name = True
        alias_generator = camelize
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
