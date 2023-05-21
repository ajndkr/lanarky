import pytest
from pydantic import ValidationError

from lanarky.schemas import Message, MessageType, Sender, WebsocketResponse


def test_websocket_response():
    response = WebsocketResponse(
        sender=Sender.BOT, message=Message.NULL, message_type=MessageType.START
    )
    assert response.sender == Sender.BOT
    assert response.message == Message.NULL
    assert response.message_type == MessageType.START

    with pytest.raises(ValidationError):
        response = WebsocketResponse(
            sender="invalid_sender",  # type: ignore
            message="invalid_message",
            message_type="invalid_type",  # type: ignore
        )

    with pytest.raises(ValidationError):
        response = WebsocketResponse(
            sender=Sender.BOT, message="invalid_message", message_type="invalid_type"  # type: ignore
        )
