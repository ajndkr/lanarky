from typing import Any, Awaitable, Callable, Dict, Union

from fastapi import WebSocket
from langchain import LLMChain
from langchain.callbacks import AsyncCallbackManager

from ..callbacks import AsyncLLMChainWebsocketCallback, AsyncWebsocketCallback
from .base import BaseLangchainWebsocketConnection, Response


class LLMChainWebsocketConnection(BaseLangchainWebsocketConnection):
    """BaseLangchainStreamingResponse class wrapper for LLMChain instances."""

    @staticmethod
    def _create_chain_executor(
        chain: LLMChain,
        inputs: Union[Dict[str, Any], Any],
        websocket: WebSocket,
        response: Response,
    ) -> Callable[[], Awaitable[Any]]:
        async def wrapper():
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
            return await chain.arun(inputs)

        return wrapper
