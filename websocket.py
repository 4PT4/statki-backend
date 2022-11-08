from fastapi import WebSocket, WebSocketDisconnect
from schemas import Message

handlers = {}


async def websocket_route(context: WebSocket, token: str):
    await context.accept()
    connect_handler = handlers.get('connect')
    if connect_handler:
        await connect_handler(context, token)
    try:
        while True:
            payload = await context.receive_json()
            message = Message(**payload)
            handler = handlers.get(message.event)
            await handler(context, message.data)
    except WebSocketDisconnect:
        disconnect_handler = handlers.get('disconnect')
        if disconnect_handler:
            await disconnect_handler(context)


def register_events(callbacks):
    for callback in callbacks:
        handlers[callback.__name__] = callback

    return websocket_route
