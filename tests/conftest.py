from unittest.mock import AsyncMock, MagicMock, create_autospec

import pytest
from fastapi import WebSocket, WebSocketDisconnect
from langchain.chains.llm import LLMChain
from starlette.types import Send

from lanarky.schemas import Message, MessageType, Sender, WebsocketResponse


@pytest.fixture(scope="function")
def send():
    return AsyncMock(spec=Send)


@pytest.fixture(scope="function")
def websocket():
    return AsyncMock(spec=WebSocket)


@pytest.fixture(scope="function")
def bot_response():
    return WebsocketResponse(
        sender=Sender.BOT, message=Message.NULL, message_type=MessageType.STREAM
    )


@pytest.fixture
def chain():
    return MagicMock(spec=LLMChain)


@pytest.fixture
def mock_websocket():
    websocket = create_autospec(WebSocket)
    websocket.accept = AsyncMock()
    websocket.receive_text = AsyncMock(side_effect=["Hello", WebSocketDisconnect()])
    websocket.send_json = AsyncMock()
    websocket.send_text = AsyncMock()
    return websocket
