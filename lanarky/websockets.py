from contextlib import asynccontextmanager
from typing import Generator

from fastapi.websockets import WebSocket, WebSocketDisconnect

from lanarky.logging import logger
from lanarky.utils import StrEnum


class DataMode(StrEnum):
    JSON = "json"
    TEXT = "text"
    BYTES = "bytes"


class WebsocketSession:
    """Class to handle websocket connections.

    Supports 3 data modes: JSON, TEXT, and BYTES.

    To know more about WebSockets, read the
    [FastAPI documentation](https://fastapi.tiangolo.com/advanced/websockets/).
    """

    @asynccontextmanager
    async def connect(
        self, websocket: WebSocket, mode: DataMode = DataMode.JSON
    ) -> Generator:
        """Connect to a websocket and yield data from it.

        Args:
            websocket: The websocket to connect to.
            mode: The data mode to use. Defaults to DataMode.JSON.

        Yields:
            Any: data from client side.
        """
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
