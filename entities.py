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

        # query = db.query(Player)
        # query = query.filter(Player.id == player.id)
        # player: Player = query.first()
        # player = player
        # player.wins += 1

        self.player: PlayerInternal = player
        self.callback = callback

    def increment_win(self):

        pass

    def increment_lose(self):
        pass

    def update_warships(self, warships: List[WarshipBase]):
        query = self.__db.query(Player)
        query = query.filter_by()

        self.player.warships = warships
