from typing import Iterator, Type
from unittest.mock import AsyncMock, create_autospec

import pytest
from starlette.types import Send

from lanarky.websockets import WebSocket


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
    websocket.send_json = AsyncMock()
    return websocket
