from typing import Any, Awaitable, Callable

from fastapi import WebSocket
from langchain import LLMChain
from langchain.callbacks import AsyncCallbackManager

from ..callbacks import AsyncLLMChainWebsocketCallback, AsyncWebsocketCallback
from ..schemas import WebsocketResponse
from .base import BaseLangchainWebsocketConnection


class LLMChainWebsocketConnection(BaseLangchainWebsocketConnection):
    """BaseLangchainStreamingResponse class wrapper for LLMChain instances."""

    @staticmethod
    def _create_chain_executor(
        chain: LLMChain,
        websocket: WebSocket,
        response: WebsocketResponse,
    ) -> Callable[[], Awaitable[Any]]:
        async def wrapper(user_message: str):
            if not isinstance(chain.llm.callback_manager, AsyncCallbackManager):
                raise TypeError(
                    "llm.callback_manager must be an instance of AsyncCallbackManager"
                )
            for handler in chain.llm.callback_manager.handlers:
                if isinstance(handler, AsyncWebsocketCallback):
                    chain.llm.callback_manager.remove_handler(handler)
                    break
            chain.llm.callback_manager.add_handler(
                AsyncLLMChainWebsocketCallback(websocket=websocket, response=response)
            )
            return await chain.arun(user_message)

        return wrapper
