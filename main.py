from fastapi import FastAPI
from event_feed import EventFeed

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
