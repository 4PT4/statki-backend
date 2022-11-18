from fastapi import Depends, FastAPI, HTTPException, status
import websocket
from fastapi.middleware import Middleware
from database import engine, Base, get_db
from models import Player
from sqlalchemy.orm import Session
from schemas import PlayerBase, Credentials, Token, ShootMessage, ReadyMessage
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from auth import verify_password, create_token, WebSocketAuthBackend
from crud import create_player
from entities import PlayerConnection
import typing
from game import Game, GameSession, GameExitCode
from utils import create_player_payload, create_init_payload

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


game = Game()


async def connect(conn: PlayerConnection, data):
    payload = create_init_payload(conn.player)
    await conn.callback("init", payload)


async def disconnect(conn: PlayerConnection, data):
    conn.increment_lose()
    game.dequeue(conn)
    enemy = game.stop_current_session(conn)
    if enemy:
        await enemy.callback("stop", {"code": GameExitCode.ENEMY_DISCONNECTED})


async def shoot(conn: PlayerConnection, data: ShootMessage):
    game_session = game.get_player_session(conn)
    if not (game_session and game_session.now_moves == conn):
        return

    did_hit, game_over = game_session.shoot(data.x, data.y)
    await conn.callback("shoot", {"hit": did_hit})
    enemy = game_session.get_enemy(conn)
    await enemy.callback("hit", {"wasHit": did_hit, "field": {"x": data.x, "y": data.y}})
    if not game_over:
        return

    game.game_sessions.remove(game_session)
    conn.increment_win()
    enemy = game_session.get_enemy(conn)
    enemy.increment_lose()
    del game_session
    await conn.callback("stop", {"code": GameExitCode.WIN})
    await enemy.callback("stop", {"code": GameExitCode.LOSE})


async def ready(conn: PlayerConnection, data: ReadyMessage):
    # conn.update_warships(data.warships)
    game_session: GameSession = game.enqueue(conn)
    if not game_session:
        return

    ally = game_session.now_moves
    enemy = game_session.get_enemy(ally)
    await ally.callback("start", create_player_payload(enemy.player))
    await enemy.callback("start", create_player_payload(ally.player))


app_websocket.add_api_websocket_route('/', websocket.register_events([
    connect,
    disconnect,
    ready,
    shoot
]))


app.mount("/", app_websocket)
