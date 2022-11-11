from fastapi import Depends, FastAPI, HTTPException, status
import websocket
from database import engine, Base, get_db
from models import Player
from sqlalchemy.orm import Session
from schemas import PlayerBase, Credentials, Token
from fastapi.middleware.cors import CORSMiddleware
from auth import get_password_hash, verify_password, create_token

Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/players", response_model=list[PlayerBase])
def get_players(seen_after: int = 0, db: Session = Depends(get_db)):
    query = db.query(Player)
    query = query.filter(Player.last_seen >= seen_after)
    query = query.order_by(Player.wins.desc())
    players = query.all()

    return players


def create_player(db: Session, credentials: Credentials):
    player = Player(
        nickname=credentials.nickname,
        password=get_password_hash(credentials.password)
    )
    db.add(player)
    db.commit()
    db.refresh(player)

    return player.id


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
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        player_id = create_player(db, credentials)

    return Token(token=create_token(player_id))


# register WebSocket endpoint
app.add_api_websocket_route('/', websocket.register_events([
    # connect,
    # disconnect,
    # ready
    # shoot
    # begin
    # end
]))
