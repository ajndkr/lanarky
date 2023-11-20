from typing import Type
from unittest.mock import AsyncMock, patch

import pytest

from lanarky.websockets import (
    DataMode,
    WebSocket,
    WebSocketDisconnect,
    WebsocketSession,
)


@pytest.mark.asyncio
async def test_connect_json(websocket: Type[WebSocket]):
    session = WebsocketSession()
    data_to_send = ["Hello", "World", "!"]
    websocket.receive_json = AsyncMock(side_effect=data_to_send)

    async with session.connect(websocket, mode=DataMode.JSON) as data_stream:
        for expected_data in data_to_send:
            received_data = await data_stream.__anext__()
            assert received_data == expected_data


@pytest.mark.asyncio
async def test_connect_text(websocket: Type[WebSocket]):
    session = WebsocketSession()
    data_to_send = ["Text", "Messages", "Here"]
    websocket.receive_text = AsyncMock(side_effect=data_to_send)

    async with session.connect(websocket, mode=DataMode.TEXT) as data_stream:
        for expected_data in data_to_send:
            received_data = await data_stream.__anext__()
            assert received_data == expected_data


@pytest.mark.asyncio
async def test_connect_bytes(websocket: Type[WebSocket]):
    session = WebsocketSession()
    data_to_send = [b"Bytes", b"Data", b"Test"]
    websocket.receive_bytes = AsyncMock(side_effect=data_to_send)

    async with session.connect(websocket, mode=DataMode.BYTES) as data_stream:
        for expected_data in data_to_send:
            received_data = await data_stream.__anext__()
            assert received_data == expected_data


@pytest.mark.asyncio
async def test_invalid_data_mode(websocket: Type[WebSocket]):
    session = WebsocketSession()

    with pytest.raises(ValueError):
        async with session.connect(websocket, mode="invalid_mode"):
            pass


@pytest.mark.asyncio
async def test_websocket_disconnect(websocket: Type[WebSocket]):
    websocket.receive_text = AsyncMock(side_effect=WebSocketDisconnect())

    with patch("lanarky.websockets.logger") as logger:
        async with WebsocketSession().connect(
            websocket, mode=DataMode.TEXT
        ) as data_stream:
            async for _ in data_stream:
                pass

        logger.info.assert_called_once_with("Websocket disconnected")
