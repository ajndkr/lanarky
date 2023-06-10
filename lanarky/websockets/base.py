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
    """Base class for websocket connections."""

    websocket: WebSocket = Field(...)
    chain_executor: Callable[[str], Awaitable[Any]] = Field(...)
    connection_accepted: bool = Field(False)

    class Config:
        arbitrary_types_allowed = True

    async def connect(self, accept_connection: bool = True):
        if accept_connection and self.connection_accepted:
            raise RuntimeError("Connection already accepted.")

        if accept_connection:
            """Connect to websocket."""
            await self.websocket.accept()
            self.connection_accepted = True

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
                logger.debug("client disconnected.")
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
        """Creates a function to execute ``chain.acall()``.

        Args:
            chain: langchain chain instance.
            websocket: websocket instance.
            response: WebsocketResponse instance.
            callback_kwargs: keyword arguments for callback function.
        """
        raise NotImplementedError

    @classmethod
    def from_chain(
        cls,
        chain: Chain,
        websocket: WebSocket,
        callback_kwargs: dict[str, Any] = {},
    ) -> "BaseWebsocketConnection":
        """Creates a BaseWebsocketConnection instance from a langchain chain instance.

        Args:
            chain: langchain chain instance.
            websocket: websocket instance.
            callback_kwargs: keyword arguments for callback function.
        """
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
        """Creates a function to execute ``chain.acall()``.

        Args:
            chain: langchain chain instance.
            websocket: websocket instance.
            response: WebsocketResponse instance.
            callback_kwargs: keyword arguments for callback function.
        """

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
