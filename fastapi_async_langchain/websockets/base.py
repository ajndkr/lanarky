"""
Credits:
- https://github.com/hwchase17/chat-langchain
- https://github.com/pors/langchain-chat-websockets
"""
import logging
from abc import abstractstaticmethod
from typing import Any, Awaitable, Callable

from fastapi import WebSocket, WebSocketDisconnect
from langchain.chains.base import Chain
from pydantic import BaseModel, Field

from ..schemas import Message, MessageType, Sender, WebsocketResponse

logger = logging.getLogger(__name__)


class BaseLangchainWebsocketConnection(BaseModel):
    websocket: WebSocket = Field(...)
    chain_executor: Callable[[], Awaitable[Any]] = Field(...)

    class Config:
        arbitrary_types_allowed = True

    async def connect(self):
        await self.websocket.accept()
        while True:
            try:
                user_message = await self.websocket.receive_text()
                await self.websocket.send_json(
                    WebsocketResponse(
                        sender=Sender.HUMAN,
                        message=user_message,
                        message_type=MessageType.STREAM,
                    ).dict()
                )
                await self.websocket.send_json(
                    WebsocketResponse(
                        sender=Sender.BOT,
                        message=Message.NULL,
                        message_type=MessageType.START,
                    ).dict()
                )
                await self.chain_executor(user_message)
                await self.websocket.send_json(
                    WebsocketResponse(
                        sender=Sender.BOT,
                        message=Message.NULL,
                        message_type=MessageType.END,
                    ).dict()
                )
            except WebSocketDisconnect:
                logger.info("client disconnected.")
                break
            except Exception as e:
                logger.error(e)
                await self.websocket.send_json(
                    WebsocketResponse(
                        sender=Sender.BOT,
                        message=Message.ERROR,
                        message_type=MessageType.ERROR,
                    ).dict()
                )

    @abstractstaticmethod
    def _create_chain_executor(
        chain: Chain,
        websocket: WebSocket,
        response: WebsocketResponse,
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
            WebsocketResponse(
                sender=Sender.BOT, message=Message.NULL, message_type=MessageType.STREAM
            ),
        )

        return cls(
            chain_executor=chain_executor,
            websocket=websocket,
        )
