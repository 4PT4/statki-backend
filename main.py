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

class GameQueue:
    def __init__(self) -> None:
        self.queue = []

    def enqueue(self, conn):
        # conn.player.id
        # ..nickname
        self.queue.append(conn)
        if len(self.queue) > 1:
            # wyciagnac dwoch ostatnich graczy z kolejki
            # stworzyc nowa sesje z tych dwoch graczy
            # session.start()
            pass

class GameSession:
    def __init__(self, player_a: PlayerConnection, player_b: PlayerConnection) -> None:
        self.player_a = player_a
        self.player_b = player_b
        # zapisywac kto w tym momencie ma ruch

        pass

    def start(self):
        # wyslac do obydwu uzytkownikow ten sam komunikat:
        # { "status": "GAME_STARTED" }
        pass

    def shoot(self, x, y):
        # czy jakikolwiek statek przeciwnika lezy w x, y
        # wyslac do uzytkownika który strzelil callback ze trafil
        # lub nie trafil
        # sprawidzic czy to byl ostatni statek na planszy
        # jesli tak uzytkownik.send({"status": "WIN"})
        # uzytkownik.wins + 1
        # i wtedy przciwnik.send({"status": "LOSE"})
        # przeciwnik.lose + 1
        # (a do przeciwnika czy dostal)
        pass


game_queue = GameQueue()


async def connect(db: Session, conn: PlayerConnection, data):
    await conn.callback("init", conn.player.warships)


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
    # session.shoot(x, y)
    pass

async def ready(db: Session, conn: PlayerConnection, data):
    game_queue.enqueue(conn)
    print(game_queue.queue)
    

app_websocket.add_api_websocket_route('/', websocket.register_events([
    connect,
    disconnect,
    ready
    # TODO: shoot
]))


app.mount("/", app_websocket)
