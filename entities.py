from models import Player


class NetworkPlayer:
    def __init__(self, data: Player, callback) -> None:
        self.data = data
        self.callback = callback
