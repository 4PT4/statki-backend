from fastapi import FastAPI
from event_feed import EventFeed
# imports for database
from fastapi import Depends, FastAPI
from database import engine
import models
from entities import Orientation

from database import get_db

models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()

# register REST endpoints
# task #2 + #6

# task #3
# game_engine: GameEngine = GameEngine()
# event_feed: EventFeed = EventFeed(game_engine)

# create WebSocket event feed
event_feed: EventFeed = EventFeed()

# register WebSocket endpoint
app.add_api_websocket_route('/', event_feed)

# Insert Data to DB
player1 = models.Player(id=1, nickname="player1", wins=2, loses=1)
player2 = models.Player(id=2, nickname="player2", wins=5, loses=2)
warship1 = models.Warship(id=1, player_id=1, length=2,
                          x=1, y=1, orientation=Orientation.HORIZONTAL)
warship2 = models.Warship(id=2, player_id=2, length=1,
                          x=3, y=3, orientation=Orientation.VERTICAL)
warship3 = models.Warship(id=3, player_id=6, length=3,
                          x=4, y=4, orientation=Orientation.HORIZONTAL)
with next(get_db()) as db:
    db.add(player1)
    db.add(player2)
    db.add(warship1)
    db.add(warship2)
    db.add(warship3)
    db.commit()
