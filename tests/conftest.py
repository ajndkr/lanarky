from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import WebSocket
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
