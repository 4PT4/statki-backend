from this import d
from fastapi import FastAPI
from event_feed import EventFeed
# imports for database
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine

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
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
