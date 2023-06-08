import json
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient

from lanarky.schemas import MessageType, Sender, WebsocketResponse
from lanarky.websockets import WebsocketConnection


def test_websocket_endpoint(chain: MagicMock):
    app = FastAPI()

    @app.websocket("/ws")
    async def endpoint(
        websocket: WebSocket,
    ) -> None:
        """Websocket chat endpoint."""
        connection = WebsocketConnection.from_chain(chain=chain, websocket=websocket)
        await connection.connect()

    client = TestClient(app)

    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("Hello")
        response = websocket.receive_text()
        assert json.loads(response) == {
            "sender": Sender.HUMAN.value,
            "message": "Hello",
            "message_type": MessageType.STREAM.value,
        }


@pytest.mark.asyncio
async def test_connect_accepts_websocket_connection_when_accept_connection_is_true(
    chain: MagicMock, mock_websocket: WebSocket
):
    connection = WebsocketConnection.from_chain(chain=chain, websocket=mock_websocket)
    await connection.connect(accept_connection=True)

    mock_websocket.accept.assert_called_once()
    mock_websocket.receive_text.assert_called_with()
    mock_websocket.send_json.assert_any_call(
        WebsocketResponse(
            sender=Sender.HUMAN,
            message="Hello",
            message_type=MessageType.STREAM,
        ).dict()
    )
    mock_websocket.send_json.assert_any_call(
        WebsocketResponse(
            sender=Sender.BOT,
            message="",
            message_type=MessageType.START,
        ).dict()
    )

    mock_websocket.send_json.assert_any_call(
        WebsocketResponse(
            sender=Sender.BOT,
            message="",
            message_type=MessageType.END,
        ).dict()
    )


@pytest.mark.asyncio
async def test_connect_accepts_websocket_connection_when_accept_connection_is_false(
    chain: MagicMock, mock_websocket: WebSocket
):
    connection = WebsocketConnection.from_chain(chain=chain, websocket=mock_websocket)
    await connection.connect(accept_connection=False)

    mock_websocket.accept.assert_not_called()
    mock_websocket.receive_text.assert_called_with()
    mock_websocket.send_json.assert_any_call(
        WebsocketResponse(
            sender=Sender.HUMAN,
            message="Hello",
            message_type=MessageType.STREAM,
        ).dict()
    )
    mock_websocket.send_json.assert_any_call(
        WebsocketResponse(
            sender=Sender.BOT,
            message="",
            message_type=MessageType.START,
        ).dict()
    )

    mock_websocket.send_json.assert_any_call(
        WebsocketResponse(
            sender=Sender.BOT,
            message="",
            message_type=MessageType.END,
        ).dict()
    )


@pytest.mark.asyncio
async def test_connect_accepts_websocket_connection_when_accept_connection_is_default(
    chain: MagicMock, mock_websocket: WebSocket
):
    connection = WebsocketConnection.from_chain(chain=chain, websocket=mock_websocket)
    await connection.connect()

    mock_websocket.accept.assert_called_once()
    mock_websocket.receive_text.assert_called_with()
    mock_websocket.send_json.assert_any_call(
        WebsocketResponse(
            sender=Sender.HUMAN,
            message="Hello",
            message_type=MessageType.STREAM,
        ).dict()
    )
    mock_websocket.send_json.assert_any_call(
        WebsocketResponse(
            sender=Sender.BOT,
            message="",
            message_type=MessageType.START,
        ).dict()
    )

    mock_websocket.send_json.assert_any_call(
        WebsocketResponse(
            sender=Sender.BOT,
            message="",
            message_type=MessageType.END,
        ).dict()
    )


@pytest.mark.asyncio
async def test_no_accept_after_websocket_connection_already_accepted(
    chain: MagicMock, mock_websocket: WebSocket
):
    connection = WebsocketConnection.from_chain(chain=chain, websocket=mock_websocket)
    await connection.connect(accept_connection=True)
    with pytest.raises(RuntimeError):
        await connection.connect(accept_connection=True)

    mock_websocket.accept.assert_called_once()
    mock_websocket.receive_text.assert_called_with()
    mock_websocket.send_json.assert_any_call(
        WebsocketResponse(
            sender=Sender.HUMAN,
            message="Hello",
            message_type=MessageType.STREAM,
        ).dict()
    )
    mock_websocket.send_json.assert_any_call(
        WebsocketResponse(
            sender=Sender.BOT,
            message="",
            message_type=MessageType.START,
        ).dict()
    )

    mock_websocket.send_json.assert_any_call(
        WebsocketResponse(
            sender=Sender.BOT,
            message="",
            message_type=MessageType.END,
        ).dict()
    )
