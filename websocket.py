from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import Message
from entities import PlayerConnection

handlers = {}


def create_callback(context: WebSocket):
    """
    Creates callback for websocket message handler.
    """
    async def callback(event: str, data: object) -> None:
        """
        Callback function, sends tansformed data back.
        """
        message = Message(event=event, data=data)
        await context.send_json(message.json())

    return callback


def create_caller(db: Session, context: WebSocket):
    """
    Creates message caller for websocket route.
    """
    callback = create_callback(context)
    
    async def caller(event: str, data=None):
        """
        Caller function, allows of easy websocket event handling.
        Invokes specific handler passing database session, player
        connection and data object.
        """
        handler = handlers.get(event)
        player = context.state.player
        if handler:
            return await handler(db, PlayerConnection(player, callback), data)
        else:
            print(f"[Warning] Calling \"{event}\" handler failed.")

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
    """
    Registers supported events.
    """
    for callback in callbacks:
        handlers[callback.__name__] = callback

    return websocket_route
