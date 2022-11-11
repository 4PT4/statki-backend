from fastapi import WebSocket, WebSocketDisconnect, Depends
from models import Player
from auth import get_current_player


async def try_call_handler(name: str, context: WebSocket, current_player: Player):
    handler = handlers.get(name)
    if handler:
        return await handler(current_player)


async def websocket_route(context: WebSocket, current_player: Player = Depends(get_current_player)):
    print(context)
    
    print(current_player.nickname)
    await context.accept()
    # await try_call_handler('connect', current_player)
    try:
        while True:
            pass
            # payload = await context.receive_json()
            # message = Message(**payload)
            # await try_call_handler(message.event)
    except WebSocketDisconnect:
        await try_call_handler('disconnect', context, current_player)
        # await context.close()


handlers = {}


def register_events(callbacks):
    for callback in callbacks:
        handlers[callback.__name__] = callback

    return websocket_route
