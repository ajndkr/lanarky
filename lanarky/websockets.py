from contextlib import asynccontextmanager
from enum import Enum

from fastapi.websockets import WebSocket, WebSocketDisconnect

from lanarky.logging import logger


class DataMode(str, Enum):
    JSON = "json"
    TEXT = "text"
    BYTES = "bytes"


class WebsocketSession:
    @asynccontextmanager
    async def connect(self, websocket: WebSocket, mode: DataMode = DataMode.JSON):
        await websocket.accept()
        try:
            if mode == DataMode.JSON:
                yield self.iter_json(websocket)
            elif mode == DataMode.TEXT:
                yield self.iter_text(websocket)
            elif mode == DataMode.BYTES:
                yield self.iter_bytes(websocket)
            else:
                raise ValueError(f"Invalid DataMode: {mode}")
        except WebSocketDisconnect:
            logger.info("Websocket disconnected")

    async def iter_text(self, websocket: WebSocket):
        while True:
            data = await websocket.receive_text()
            yield data

    async def iter_bytes(self, websocket: WebSocket):
        while True:
            data = await websocket.receive_bytes()
            yield data

    async def iter_json(self, websocket: WebSocket):
        while True:
            data = await websocket.receive_json()
            yield data
