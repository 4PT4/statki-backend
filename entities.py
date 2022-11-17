from schemas import PlayerInternal
from sqlalchemy.orm import Session


class PlayerConnection:
    """
    Player data structure for websocket connections,
    holds associated data and connection itself.
    """

    def __init__(self, db: Session, player: PlayerInternal, callback) -> None:
        self.__db = db
        self.player: PlayerInternal = player
        self.callback = callback

    def update_warships():
        pass
