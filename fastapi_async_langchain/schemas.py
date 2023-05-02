from enum import Enum
from typing import Union

from pydantic import BaseModel


class Sender(str, Enum):
    BOT = "bot"
    HUMAN = "human"


class Message(str, Enum):
    NULL = ""
    ERROR = "Sorry, something went wrong. Try again."


class MessageType(str, Enum):
    START = "start"
    STREAM = "stream"
    END = "end"
    ERROR = "error"
    INFO = "info"


class WebsocketResponse(BaseModel):
    sender: Sender
    message: Union[Message, str]
    message_type: MessageType

    class Config:
        use_enum_values = True
