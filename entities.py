from schemas import PlayerInternal


class PlayerConnection:
    """
    Player data structure for websocket connections,
    holds associated data and connection itself.
    """

    def __init__(self, player: PlayerInternal, callback) -> None:
        self.player: PlayerInternal = player
        self.callback = callback
