from enum import Enum
from typing import Union

from pydantic import BaseModel


class Sender(str, Enum):
    """Sender of a websocket message."""

    BOT = "bot"
    HUMAN = "human"


class Message(str, Enum):
    """Message types for websocket messages."""

    NULL = ""
    ERROR = "Sorry, something went wrong. Try again."


class MessageType(str, Enum):
    """Message types for websocket messages."""

    START = "start"
    STREAM = "stream"
    END = "end"
    ERROR = "error"
    INFO = "info"


class WebsocketResponse(BaseModel):
    """Websocket response."""

    sender: Sender
    message: Union[Message, str]
    message_type: MessageType

    class Config:
        use_enum_values = True
