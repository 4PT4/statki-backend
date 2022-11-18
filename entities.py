from schemas import PlayerInternal, WarshipBase
from sqlalchemy.orm import Session
from models import Player
from typing import List


class PlayerConnection:
    """
    Player data structure for websocket connections,
    holds associated data and connection itself.
    Has database access.
    """

    def __init__(self, db: Session, player: PlayerInternal, callback) -> None:
        self.__db = db

        total_ships = 0
        for warship in player.warships:
            total_ships += warship.length

        self.ships_left = total_ships

        query = db.query(Player)
        query = query.filter(Player.id == player.id)
        p = query.first()
        self.p: Player = p

        
        self.player: PlayerInternal = player
        self.callback = callback

    def increment_win(self):
        self.p.wins = Player.wins + 1
        self.update()

    def increment_lose(self):
        self.p.loses = Player.loses + 1
        self.update()

    def update(self):
        self.__db.add(self.p)
        self.__db.commit()
        self.__db.refresh(self.p)

    def update_warships(self, warships: List[WarshipBase]):
        query = self.__db.query(Player)
        query = query.filter_by()

        self.player.warships = warships
