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
        self.player: PlayerInternal = player
        self.callback = callback

    def add_win(self):
        pass

    def add_lose(self):
        pass

    def update_warships(self, warships: List[WarshipBase]):
        query = self.__db.query(Player)
        query = query.filter_by()

        self.player.warships = warships
