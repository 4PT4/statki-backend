from pydantic import BaseModel, Field
from humps import camelize
from typing import List
import models


class WebSocketMessage(BaseModel):
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
    last_seen: int = Field(alias="lastSeen")

    class Config:
        allow_population_by_field_name = True
        alias_generator = camelize
        orm_mode = True


class WarshipBase(BaseModel):
    id: str
    length:  int
    x: int
    y: int
    orientation: models.Orientation

    class Config:
        orm_mode = True


class ReadyMessage(BaseModel):
    warships: List[WarshipBase]


class ShootMessage(BaseModel):
    x: int
    y: int


class PlayerInternal(PlayerBase):
    warships: List[WarshipBase]
