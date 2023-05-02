"""
Credits:
- https://github.com/hwchase17/chat-langchain
- https://github.com/pors/langchain-chat-websockets
"""
import logging
from abc import abstractstaticmethod
from enum import Enum
from typing import Any, Awaitable, Callable, Dict, Union

from fastapi import WebSocket, WebSocketDisconnect
from langchain.chains.base import Chain
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


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


class Response(BaseModel):
    sender: Sender
    message: Union[Message, str]
    message_type: MessageType

    class Config:
        use_enum_values = True


class BaseLangchainWebsocketConnection(BaseModel):
    websocket: WebSocket = Field(...)
    chain_executor: Callable[[], Awaitable[Any]] = Field(...)

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    async def connect(self):
        await self.websocket.accept()
        while True:
            try:
                user_message = await self.websocket.receive_text()
                await self.websocket.send_json(
                    Response(
                        sender=Sender.HUMAN,
                        message=user_message,
                        type=MessageType.STREAM,
                    ).dict()
                )
                await self.websocket.send_json(
                    Response(
                        sender=Sender.BOT, message=Message.NULL, type=MessageType.START
                    ).dict()
                )
                await self.chain_executor(user_message)
                await self.websocket.send_json(
                    Response(
                        sender=Sender.BOT, message=Message.NULL, type=MessageType.END
                    ).dict()
                )
            except WebSocketDisconnect:
                logger.info("client disconnected.")
                break
            except Exception as e:
                logger.error(e)
                await self.websocket.send_json(
                    Response(
                        sender=Sender.BOT, message=Message.ERROR, type=MessageType.ERROR
                    ).dict()
                )

    @abstractstaticmethod
    def _create_chain_executor(
        chain: Chain,
        inputs: Union[Dict[str, Any], Any],
        websocket: WebSocket,
        response: Response,
    ) -> Callable[[str], Awaitable[Any]]:
        raise NotImplementedError

    @classmethod
    def from_chain(
        cls,
        chain: Chain,
        websocket: WebSocket,
    ) -> "BaseLangchainWebsocketConnection":
        chain_executor = cls._create_chain_executor(
            chain,
            websocket,
            Response(sender=Sender.BOT, message=Message.NULL, type=MessageType.STREAM),
        )

        return cls(
            chain_executor=chain_executor,
            websocket=websocket,
        )
