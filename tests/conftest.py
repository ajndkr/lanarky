from typing import Iterator, Type
from unittest.mock import AsyncMock, create_autospec

import pytest
from starlette.types import Send

from lanarky.websockets import WebSocket, WebSocketDisconnect


@pytest.fixture(scope="function")
def send() -> Send:
    return AsyncMock(spec=Send)


@pytest.fixture(scope="function")
def body_iterator() -> Iterator[bytes]:
    async def iterator():
        yield b"Chunk 1"
        yield b"Chunk 2"

    return iterator()


@pytest.fixture(scope="function")
def websocket() -> Type[WebSocket]:
    websocket: Type[WebSocket] = create_autospec(WebSocket)
    websocket.accept = AsyncMock()
    websocket.receive_text = AsyncMock(side_effect=["Hello", WebSocketDisconnect()])
    websocket.send_json = AsyncMock()
    websocket.send_text = AsyncMock()
    return websocket
