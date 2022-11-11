from fastapi import WebSocket, WebSocketDisconnect, Depends
from models import Player
from sqlalchemy.orm import Session
from database import get_db
from schemas import Message

handlers = {}


def create_callback(context: WebSocket):
    async def callback(event, data):
        message = Message(event=event, data=data)
        await context.send_json(message.json())

    return callback


def create_caller(db: Session, context: WebSocket):
    async def caller(event: str, data=None):
        handler = handlers.get(event)
        player = context.state.player
        callback = create_callback(context)
        if handler:
            return await handler(callback, db, player, data)
        else:
            print(f"Calling \"{event}\" handler failed.")

    return caller


async def websocket_route(context: WebSocket, db: Session = Depends(get_db)):
    await context.accept()
    caller = create_caller(db, context)
    await caller('connect')
    try:
        while True:
            payload = await context.receive_json()
            message = Message(**payload)
            await caller(message.event, message.data)
    except WebSocketDisconnect:
        await caller('disconnect')


def register_events(callbacks):
    for callback in callbacks:
        handlers[callback.__name__] = callback

    return websocket_route
