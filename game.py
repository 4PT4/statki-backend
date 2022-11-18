from entities import PlayerConnection
from sqlalchemy.orm import Session
from models import Orientation
from enum import Enum


class GameExitCode(Enum):
    UNKNOWN = 0
    WIN = 1
    LOSE = 2
    ENEMY_DISCONNECTED = 3


class GameSession:
    def __init__(self, conn_a: PlayerConnection, conn_b: PlayerConnection) -> None:
        self.conn_a = conn_a
        self.conn_b = conn_b
        # board_a
        # board_b
        self.now_moves: PlayerConnection = self.conn_a

    def shoot(self, x: int, y: int):
        """
        Shoots enemy warship.
        """
        enemy = self.get_enemy(self.now_moves)
        for warship in enemy.player.warships:
            for i in range(warship.length):
                _x = warship.x
                _y = warship.y

                if warship.orientation == Orientation.HORIZONTAL:
                    _x += i
                elif warship.orientation == Orientation.VERTICAL:
                    _y += i

                if _x == x and _y == y:
                    #            sprawdzac czy to ostatni statek na planszy
                    return True, True

        self.now_moves = enemy
        return False, False

    def destroy(self, caller: PlayerConnection) -> PlayerConnection:
        """
        Destroys game session. Returns enemy.
        """
        enemy = self.get_enemy(caller)
        return enemy

    def get_enemy(self, conn: PlayerConnection) -> PlayerConnection:
        """
        Returns enemy connection.
        """
        return self.conn_b if self.conn_a == conn else self.conn_a


class Game:
    def __init__(self) -> None:
        self.queue: list[PlayerConnection] = []
        self.game_sessions: list[GameSession] = []

    def enqueue(self, conn: PlayerConnection) -> Session | None:
        """
        Enqueues player.
        """
        if conn in self.queue:
            return

        self.queue.append(conn)
        if len(self.queue) > 1:
            player_a, player_b = self.queue[:2]
            self.queue = self.queue[2:]
            game_session = GameSession(player_a, player_b)
            self.game_sessions.append(game_session)
            return game_session

    def dequeue(self, conn: PlayerConnection) -> None:
        """
        Dequeues player if he's in queue.
        """
        if conn in self.queue:
            self.queue.remove(conn)

    def stop_current_session(self, conn: PlayerConnection) -> PlayerConnection:
        """
        Stops current game session. Returns enemy.
        """
        for session in self.game_sessions:
            if conn in [session.conn_a, session.conn_b]:
                enemy = session.destroy(conn)
                self.game_sessions.remove(session)
                del session
                return enemy

    def get_player_session(self, conn: PlayerConnection) -> GameSession | None:
        """
        Returns game session if it's provided player' turn.
        """
        for session in self.game_sessions:
            if session.now_moves == conn:
                return session
