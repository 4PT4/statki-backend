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





# connecting files associated with database




#Insert Data to DB

 

Player_insert1 = models.Player(id = 1, nickname="player1", wins=2, loses=1)
Player_insert2 = models.Player(id = 2, nickname="player2", wins=5, loses=2)


Warship_Insert1 = models.Warship(id = 1, player_id=1, length=2, x=1,y=1, orientation=Orientation.HORIZONTAL)
Warship_Insert2 = models.Warship(id = 2, player_id=2, length=1, x=3,y=3, orientation=Orientation.VERTICAL)
Warship_Insert3 = models.Warship(id = 3, player_id=6, length=3, x=4,y=4, orientation=Orientation.HORIZONTAL)

with next(get_db()) as db:
    db.add(Player_insert1)
    db.add(Player_insert2)
    db.add(Warship_Insert1)
    db.add(Warship_Insert2)
    db.add(Warship_Insert3)
    db.commit()
    
