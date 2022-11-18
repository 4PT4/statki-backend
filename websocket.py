from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas
from entities import PlayerConnection
from humps import camelize
import typing
import json

handlers = {}


def create_callback(context: WebSocket):
    """
    Creates callback for websocket message handler.
    """
    async def callback(event: str, data: object) -> None:
        """
        Callback function, sends tansformed data back.
        """
        message = schemas.Message(event=event, data=data)
        await context.send_json(message.json())

    return callback


def create_caller(db: Session, context: WebSocket):
    """
    Creates message caller for websocket route.
    """
    async def caller(event: str, data=None):
        """
        Caller function, allows of easy websocket event handling.
        Invokes specific handler passing database session, player
        connection and data object.
        """
        handler = handlers.get(event)
        if not handler:
            print(f"[Warning] No handler named \"{event}\" was registered.")
            return
        
        types = typing.get_type_hints(handler)
        try:
            DataType = types['data']
            if not issubclass(DataType, schemas.BaseModel):
                raise TypeError

            data = DataType(**data)
        except KeyError:
            pass
        except TypeError:
            print(f"[Warning] Incorrect type was specified in \"{event}\" handler. Unable to deserialize.")

        player = context.state.player
        callback = create_callback(context)
        player_connection = PlayerConnection(player, callback)

        return await handler(db, player_connection, data)

    return caller


async def websocket_route(context: WebSocket, db: Session = Depends(get_db)):
    await context.accept()
    caller = create_caller(db, context)
    await caller('connect')
    try:
        while True:
            try:
                payload = await context.receive_json()
                message = schemas.Message(**payload)
                await caller(message.event, message.data)
            except json.decoder.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        await caller('disconnect')


def register_events(callbacks):
    """
    Registers supported events.
    """
    for callback in callbacks:
        handlers[camelize(callback.__name__)] = callback

    return websocket_route
