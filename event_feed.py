from fastapi import WebSocket, WebSocketDisconnect
import schemas


class EventFeed:
    async def __call__(self, context: WebSocket) -> None:
        await context.accept()
        try:
            while True:
                payload = await context.receive_json()
                message = schemas.Message(**payload)
                # temporary solution
                handler = getattr(self, message.event)
                await handler(context, message.data)
        except WebSocketDisconnect:
            await self.disconnect(context)

    async def ready(self, context: WebSocket, data):
        # task #5 / frontend #6
        pass

    async def fire(self, context: WebSocket, data):
        # task #5 / frontend #1
        pass

    async def start(self, context: WebSocket, data):
        # task #3
        pass

    async def disconnect(self, context: WebSocket):
        # task #3
        pass
