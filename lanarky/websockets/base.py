"""
Credits:

* `chat-langchain <https://github.com/hwchase17/chat-langchain>`_
* `langchain-chat-websockets <https://github.com/pors/langchain-chat-websockets>`_
"""
import logging
from typing import Any, Awaitable, Callable

from fastapi import WebSocket, WebSocketDisconnect
from langchain.chains.base import Chain
from pydantic import BaseModel, Field

from lanarky.callbacks import get_websocket_callback
from lanarky.schemas import Message, MessageType, Sender, WebsocketResponse

logger = logging.getLogger(__name__)


class BaseWebsocketConnection(BaseModel):
    websocket: WebSocket = Field(...)
    chain_executor: Callable[[str], Awaitable[Any]] = Field(...)

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

    @staticmethod
    def _create_chain_executor(
        chain: Chain,
        websocket: WebSocket,
        response: WebsocketResponse,
        **callback_kwargs,
    ) -> Callable[[str], Awaitable[Any]]:
        raise NotImplementedError

    @classmethod
    def from_chain(
        cls,
        chain: Chain,
        websocket: WebSocket,
        callback_kwargs: dict[str, Any] = {},
    ) -> "BaseWebsocketConnection":
        chain_executor = cls._create_chain_executor(
            chain,
            websocket,
            WebsocketResponse(
                sender=Sender.BOT, message=Message.NULL, message_type=MessageType.STREAM
            ),
            **callback_kwargs,
        )

        return cls(
            chain_executor=chain_executor,
            websocket=websocket,
        )


class WebsocketConnection(BaseWebsocketConnection):
    """BaseLangchainStreamingResponse class wrapper for LLMChain instances."""

    @staticmethod
    def _create_chain_executor(
        chain: Chain,
        websocket: WebSocket,
        response: WebsocketResponse,
        **callback_kwargs,
    ) -> Callable[[str], Awaitable[Any]]:
        async def wrapper(user_message: str):
            return await chain.acall(
                inputs=user_message,
                callbacks=[
                    get_websocket_callback(
                        chain=chain,
                        websocket=websocket,
                        response=response,
                        **callback_kwargs,
                    )
                ],
            )

        return wrapper
