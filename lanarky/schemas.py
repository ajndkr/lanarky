from enum import Enum
from typing import Any, Union

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


class StreamingJSONResponse(BaseModel):
    token: str = ""


class BaseRetrievalQAStreamingJSONResponse(StreamingJSONResponse):
    source_documents: list[dict[str, Any]]
