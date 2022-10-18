from fastapi import FastAPI
from event_feed import EventFeed
# imports for database
from fastapi import Depends, FastAPI
from database import engine
from models import * 
import models

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



#Creates database
Base.metadata.create_all(engine)

#Insert Data to DB

Player_insert1 = models.Player(id = "1", nickname="player1", wins="2", loses="1", last_seen="2022/10/15")
Player_insert2 = models.Player(id = "2", nickname="player2", wins="5", loses="2", last_seen="2022/10/15")



Warship_Insert1 = models.Warship(id="1", player_id="1", length="2", x="1",y="1", orientation="1")
Warship_Insert2 = models.Warship(id="2", player_id="2", length="1", x="3",y="3", orientation="2")
Warship_Insert3 = models.Warship(id="3", player_id="2", length="3", x="4",y="4", orientation="1")


                                                       