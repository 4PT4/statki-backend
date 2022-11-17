from enum import Enum
from fastapi import Depends, FastAPI, HTTPException, status
import websocket
from fastapi.middleware import Middleware
from database import engine, Base, get_db
from models import Player
from sqlalchemy.orm import Session
from schemas import PlayerBase, Credentials, Token
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from auth import verify_password, create_token, WebSocketAuthBackend
from crud import create_player
from entities import PlayerConnection
import typing

Base.metadata.create_all(bind=engine)

middleware = [
    Middleware(CORSMiddleware,
               allow_origins=["*"],
               allow_methods=["*"],
               allow_headers=["*"])
]

app: FastAPI = FastAPI(middleware=middleware)


@app.get("/players", response_model=typing.List[PlayerBase])
def get_players(seen_after: int = 0, db: Session = Depends(get_db)):
    query = db.query(Player)
    query = query.filter(Player.last_seen >= seen_after)
    query = query.order_by(Player.wins.desc())
    players = query.all()

    return players


@app.post("/auth/login", response_model=Token)
def login(credentials: Credentials, db: Session = Depends(get_db)):
    query = db.query(Player)
    query = query.filter(Player.nickname == credentials.nickname)
    player: Player = query.first()

    player_id = None

    if player:
        if verify_password(credentials.password, player.password):
            player_id = player.id
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password."
            )
    else:
        player_id = create_player(db, credentials)

    return Token(token=create_token(player_id))


websocket_middleware = [
    *middleware,
    Middleware(AuthenticationMiddleware,
               backend=WebSocketAuthBackend())
]

app_websocket: FastAPI = FastAPI(
    middleware=websocket_middleware)


# zmienmy nawe tego, to juz nie bedzie tylko kolejka, ale cala "gra"
# oprocz dodawania osob do kolejki tutaj powinnismy obslugiwac oddawanie strzalow
# "shoot" z sesji przeniesc tutaj
class GameQueue:
    def __init__(self) -> None:
        self.queue = []
        self.game_sessions: list[GameSession] = []

    def enqueue(self, conn):
        self.queue.append(conn)
        if len(self.queue) > 1:
            player_a, player_b = self.queue[:2]
            self.queue = self.queue[2:]
            game_session = GameSession(self, player_a, player_b)
            self.game_sessions.append(game_session)
            game_session.start()

    def dequeue(self, conn):

        pass

    def shoot(self, conn: PlayerConnection, x: int, y: int) -> bool:

        for session in self.game_sessions:
            if session.contains(conn):
                session.shoot(x,y)



        # czy jakikolwiek statek przeciwnika lezy w x, y
        # wyslac do uzytkownika który strzelil callback ze trafil
        # lub nie trafil
        # sprawidzic czy to byl ostatni statek na planszy
        # jesli tak uzytkownik.send({"status": "WIN"})
        # uzytkownik.wins + 1
        # i wtedy przciwnik.send({"status": "LOSE"})
        # przeciwnik.lose + 1
        # (a do przeciwnika czy dostal)


class GameSession:
    def __init__(self, ally: PlayerConnection, enemy: PlayerConnection) -> None:
        self.ally: PlayerConnection = ally
        self.enemy: PlayerConnection = enemy

        self.now_moves = self.ally

    def start(self):
        self.ally.callback(WebSocketEvent.START, self.enemy.player.nickname)
        self.enemy.callback(WebSocketEvent.START, self.ally.player.nickname)
    
    def shoot (self, x, y):

        for warship in warships:
            if warship.x == x and warship.y == y:
                session1.hit()
        pass

    def hit(self):
        self.ally.callback(WebSocketEvent.HIT, { "wasHit": True })
        #self.enemy.callback(WebSocketEvent.GOT_HIT, )

    def constains(self, player: PlayerConnection):
        if self.now_moves == player:
            return True
        return False


class GameStatus(Enum):
    UNKNOWN = 0
    WIN = 1
    LOSE = 2
    ENEMY_DISCONNECTED = 3


class WebSocketEvent(Enum):
    UNKNOWN = 0
    START = 1
    HIT = 2
    GOT_HIT = 3


game_queue = GameQueue()


async def connect(db: Session, conn: PlayerConnection, data):
    await conn.callback("init", "hi")


async def disconnect(db: Session, conn: PlayerConnection, data):
    # znowu szukac czy uzytkownik jest w sesji
    # jesli jest w sesji to przeciwikowi odsylamy komunikat
    # { "status": "ENEMY_DISCONNECTED" }
    pass


async def shoot(db: Session, conn: PlayerConnection, data):
    # data zawiera to: { x: 0, y: 2 }
    # sprawdzic czy uzytkownik jest w tym momencie w sesji gry
    # jesli tak sprwaidzic czy teraz jego ruch
    # strzeclic w pole przciwnika
    # session.shoot(conn, x, y)
    pass


async def ready(db: Session, conn: PlayerConnection, data):
    # update statków gracza jesli ułożenie się zmieniło
    game_queue.enqueue(conn)


app_websocket.add_api_websocket_route('/', websocket.register_events([
    connect,
    disconnect,
    ready
    # TODO: shoot
]))


app.mount("/", app_websocket)
