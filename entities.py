from schemas import PlayerInternal, WarshipBase
from sqlalchemy.orm import Session
from models import Player, Warship
from typing import List


class PlayerConnection:
    """
    Player data structure for websocket connections,
    holds associated data and connection itself.
    Has database access.
    """

    def __init__(self, db: Session, player: Player, callback) -> None:
        self.__db = db
        self.__player = player
        self.callback = callback
        db.add(player)

        total_ships = 0
        for warship in player.warships:
            total_ships += warship.length

        self.ships_left = total_ships

    def get_player(self) -> PlayerInternal:
        return PlayerInternal(**self.__player.__dict__)

    def increment_wins(self) -> None:
        self.__player.wins = Player.wins + 1
        self.update()

    def increment_loses(self) -> None:
        self.__player.loses = Player.loses + 1
        self.update()

    def update(self) -> None:
        self.__db.add(self.__player)
        self.__db.commit()
        self.__db.refresh(self.__player)

    def update_warships(self, warships: List[WarshipBase]) -> None:
        for warship in warships:
            query = self.__db.query(Warship)
            query = query.filter(Warship.id == warship.id)
            query.update(warship.dict())

        self.update()
