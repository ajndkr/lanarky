from typing import Any, Awaitable, Callable, Dict, Union

from fastapi import WebSocket
from langchain.callbacks import AsyncCallbackManager
from langchain.chains.retrieval_qa.base import BaseRetrievalQA

from ..callbacks import (
    AsyncLLMChainWebsocketCallback,
    AsyncRetrievalQAWebsocketCallback,
    AsyncWebsocketCallback,
)
from .base import BaseLangchainWebsocketConnection, Response


class RetrievalQAWebsocketConnection(BaseLangchainWebsocketConnection):
    """BaseLangchainWebsocketConnection class wrapper for BaseRetrievalQA instances."""

    @staticmethod
    def _create_chain_executor(
        chain: BaseRetrievalQA,
        inputs: Union[Dict[str, Any], Any],
        websocket: WebSocket,
        response: Response,
    ) -> Callable[[], Awaitable[Any]]:
        async def wrapper():
            if not isinstance(
                chain.combine_documents_chain.llm_chain.llm.callback_manager,
                AsyncCallbackManager,
            ):
                raise TypeError(
                    "llm.callback_manager must be an instance of AsyncCallbackManager"
                )
            for (
                handler
            ) in chain.combine_documents_chain.llm_chain.llm.callback_manager.handlers:
                if isinstance(handler, AsyncWebsocketCallback):
                    chain.combine_documents_chain.llm_chain.llm.callback_manager.remove_handler(
                        handler
                    )
                    break
            chain.combine_documents_chain.llm_chain.llm.callback_manager.add_handler(
                AsyncLLMChainWebsocketCallback(websocket=websocket, response=response)
            )

            if not isinstance(chain.callback_manager, AsyncCallbackManager):
                raise TypeError(
                    "chain.callback_manager must be an instance of AsyncCallbackManager"
                )
            for handler in chain.callback_manager.handlers:
                if isinstance(handler, AsyncWebsocketCallback):
                    chain.callback_manager.remove_handler(handler)
                    break
            chain.callback_manager.add_handler(
                AsyncRetrievalQAWebsocketCallback(
                    websocket=websocket, response=response
                )
            )

            return await chain.acall(inputs)

        return wrapper
