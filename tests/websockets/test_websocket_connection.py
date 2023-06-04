import json
from unittest.mock import MagicMock

from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient

from lanarky.schemas import MessageType, Sender
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
