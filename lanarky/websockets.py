from contextlib import asynccontextmanager
from enum import Enum

from fastapi.websockets import WebSocket, WebSocketDisconnect


class DataMode(str, Enum):
    TEXT = "text"
    BYTES = "bytes"
    JSON = "json"


class WebsocketManager:
    def __init__(self) -> None:
        self.active_sessions: list[WebSocket] = []

    @asynccontextmanager
    async def connect(self, websocket: WebSocket, mode: DataMode = DataMode.TEXT):
        await self.accept(websocket)
        try:
            if mode == DataMode.TEXT:
                yield self.iter_text(websocket)
            elif mode == DataMode.BYTES:
                yield self.iter_bytes(websocket)
            elif mode == DataMode.JSON:
                yield self.iter_json(websocket)
            else:
                raise ValueError(f"Invalid DataMode: {mode}")
        except WebSocketDisconnect:
            self.disconnect(websocket)

    async def accept(self, websocket: WebSocket):
        await websocket.accept()
        self.active_sessions.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_sessions.remove(websocket)

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
