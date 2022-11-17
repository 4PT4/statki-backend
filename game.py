from entities import PlayerConnection
from sqlalchemy.orm import Session

class GameSession:
    def __init__(self, conn_a: PlayerConnection, conn_b: PlayerConnection) -> None:
        self.conn_a = conn_a
        self.conn_b = conn_b
        self.now_moves: PlayerConnection = self.conn_a

    def shoot(self, x: int, y: int) -> bool:
        enemy = self.get_enemy()
        for warship in enemy.player.warships:
            if warship.x == x and warship.y == y:
                return True

        self.now_moves = enemy
        return False

    def get_enemy(self) -> PlayerConnection:
        return self.conn_b if self.now_moves == self.conn_a else self.conn_a


class Game:
    def __init__(self) -> None:
        self.queue: list[PlayerConnection] = []
        self.game_sessions: list[GameSession] = []

    def enqueue(self, conn) -> Session | None:
        if conn in self.queue:
            return
        
        self.queue.append(conn)
        if len(self.queue) > 1:
            player_a, player_b = self.queue[:2]
            self.queue = self.queue[2:]
            game_session = GameSession(player_a, player_b)
            self.game_sessions.append(game_session)
            return game_session

    def dequeue(self, conn) -> None:
        pass
        # if conn in self.queue:
        #     self.queue.remove(conn)

    def get_player_session(self, conn: PlayerConnection) -> GameSession | None:
        for session in self.game_sessions:
            if session.now_moves == conn:
                return session


# czy jakikolwiek statek przeciwnika lezy w x, y
# wyslac do uzytkownika który strzelil callback ze trafil
# lub nie trafil
# sprawidzic czy to byl ostatni statek na planszy
# jesli tak uzytkownik.send({"status": "WIN"})
# uzytkownik.wins + 1
# i wtedy przciwnik.send({"status": "LOSE"})
# przeciwnik.lose + 1
# (a do przeciwnika czy dostal)


# class GameStatus(Enum):
#     UNKNOWN = 0
#     WIN = 1
#     LOSE = 2
#     ENEMY_DISCONNECTED = 3