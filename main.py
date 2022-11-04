from fastapi import FastAPI, Depends
from event_feed import EventFeed
from database import engine, Base, get_db
from models import Warship, Player
from entities import Orientation
from sqlalchemy.orm import Session
from schemas import PlayerBase
import time
import math
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register REST endpoints
# task #2 + #6


@app.get("/players", response_model=list[PlayerBase])
def get_players(seen_after: int = 0, db: Session = Depends(get_db)):
    players = db.query(Player).filter(Player.last_seen >= seen_after).all()
    return players

# task #3
# game_engine: GameEngine = GameEngine()
# event_feed: EventFeed = EventFeed(game_engine)


# create WebSocket event feed
event_feed: EventFeed = EventFeed()

# register WebSocket endpoint
app.add_api_websocket_route('/', event_feed)

# Insert Data to DB
timestamp = time.time()
timestamp = math.floor(timestamp)
player1 = Player(id=1, nickname="player1", wins=2,
                 loses=1, last_seen=timestamp)
player2 = Player(id=2, nickname="player2", wins=5,
                 loses=2, last_seen=timestamp)
warship1 = Warship(id=1, player_id=1, length=2, x=1, y=1,
                   orientation=Orientation.HORIZONTAL)
warship2 = Warship(id=2, player_id=2, length=1, x=3,
                   y=3, orientation=Orientation.VERTICAL)
warship3 = Warship(id=3, player_id=6, length=3, x=4, y=4,
                   orientation=Orientation.HORIZONTAL)

with next(get_db()) as db:
    db.add(player1)
    db.add(player2)
    db.add(warship1)
    db.add(warship2)
    db.add(warship3)
    db.commit()
